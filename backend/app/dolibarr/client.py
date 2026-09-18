"""Client HTTP centralise vers l'API REST Dolibarr.

Toute la logique d'acces a Dolibarr (auth, timeout, retry, gestion des
erreurs, logs) est concentree ici. Aucun autre module du backend ne doit
appeler `httpx` directement vers Dolibarr : les services metier (voir
`app/services/`) passent systematiquement par `DolibarrClient`.

Reference: https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_(developer)
La cle API est envoyee dans le header `DOLAPIKEY`, jamais en query string,
pour eviter qu'elle ne se retrouve dans des logs d'acces ou des URLs
partagees.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.config import Settings, get_settings
from app.dolibarr.exceptions import (
    DolibarrAuthError,
    DolibarrClientError,
    DolibarrConnectionError,
    DolibarrNotFoundError,
    DolibarrTimeoutError,
)

logger = logging.getLogger("mga.dolibarr")

# Nombre de tentatives pour les methodes idempotentes (GET) en cas d'erreur
# reseau ou 5xx. Les methodes non-idempotentes (POST/PUT/DELETE) ne sont
# JAMAIS retentees automatiquement ici : une couche superieure doit gerer
# l'idempotence via une cle dediee (voir strategie offline, ARCHITECTURE.md).
_MAX_RETRIES_READ = 2


class DolibarrClient:
    """Client bas niveau pour l'API REST Dolibarr."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._client = httpx.Client(
            base_url=self._settings.dolibarr_api_url,
            timeout=self._settings.dolibarr_timeout_seconds,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "DolibarrClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # -- API publique --------------------------------------------------

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params, retryable=True)

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("POST", path, json=json, retryable=False)

    def put(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("PUT", path, json=json, retryable=False)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path, retryable=False)

    # -- Interne ----------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        return {
            "DOLAPIKEY": self._settings.dolibarr_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        retryable: bool,
    ) -> Any:
        url = path if path.startswith("/") else f"/{path}"
        attempts = _MAX_RETRIES_READ + 1 if retryable else 1
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            try:
                response = self._client.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=self._headers(),
                )
                return self._handle_response(method, url, response)
            except httpx.TimeoutException as exc:
                last_error = exc
                logger.warning(
                    "dolibarr_timeout method=%s path=%s attempt=%s/%s",
                    method,
                    url,
                    attempt,
                    attempts,
                )
                if attempt == attempts:
                    raise DolibarrTimeoutError(
                        f"Timeout en appelant Dolibarr ({method} {url})"
                    ) from exc
            except httpx.TransportError as exc:
                last_error = exc
                logger.warning(
                    "dolibarr_connection_error method=%s path=%s attempt=%s/%s error=%s",
                    method,
                    url,
                    attempt,
                    attempts,
                    exc.__class__.__name__,
                )
                if attempt == attempts:
                    raise DolibarrConnectionError(
                        f"Impossible de joindre Dolibarr ({method} {url})"
                    ) from exc

        # Ne devrait jamais etre atteint : la boucle retourne ou leve avant.
        raise DolibarrClientError(str(last_error) if last_error else "Erreur inconnue")

    def _handle_response(self, method: str, url: str, response: httpx.Response) -> Any:
        # Ne jamais logger le contenu du header DOLAPIKEY ni le corps brut
        # (peut contenir des donnees client sensibles) : on ne logue que le
        # statut et la route.
        logger.info("dolibarr_call method=%s path=%s status=%s", method, url, response.status_code)

        if response.status_code in (401, 403):
            raise DolibarrAuthError(
                "Authentification Dolibarr refusee (DOLAPIKEY invalide ou droits insuffisants)",
                status_code=response.status_code,
            )
        if response.status_code == 404:
            raise DolibarrNotFoundError(f"Ressource Dolibarr introuvable: {url}", status_code=404)
        if response.status_code >= 400:
            raise DolibarrClientError(
                f"Erreur Dolibarr {response.status_code} sur {method} {url}",
                status_code=response.status_code,
            )
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise DolibarrClientError(
                f"Reponse Dolibarr non-JSON sur {method} {url}"
            ) from exc


_client_singleton: DolibarrClient | None = None


def get_dolibarr_client() -> DolibarrClient:
    """Dependance FastAPI: retourne une instance partagee de DolibarrClient."""
    global _client_singleton
    if _client_singleton is None:
        _client_singleton = DolibarrClient()
    return _client_singleton
