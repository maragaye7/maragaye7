class DolibarrClientError(Exception):
    """Erreur generique lors d'un appel a l'API Dolibarr."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class DolibarrAuthError(DolibarrClientError):
    """DOLAPIKEY invalide ou manquante (401/403)."""


class DolibarrNotFoundError(DolibarrClientError):
    """Ressource introuvable cote Dolibarr (404)."""


class DolibarrConnectionError(DolibarrClientError):
    """Impossible de joindre le serveur Dolibarr (reseau, DNS, TLS...)."""


class DolibarrTimeoutError(DolibarrClientError):
    """Le serveur Dolibarr n'a pas repondu dans le delai imparti."""
