"""Service de gestion des clients (tiers Dolibarr).

Mapping MGA <-> Dolibarr documente dans ARCHITECTURE.md section 6.
GET /thirdparties : recherche via `sqlfilters`.

TODO(dolibarr-api): la syntaxe exacte de `sqlfilters` combinant plusieurs
champs (nom OU email OU telephone) doit etre validee contre l'instance
reelle (https://mgassistances.com/crm) avant la mise en production. En
attendant, on construit un filtre sur `nom` uniquement, le filtrage
supplementaire (email/tel) est fait cote MGA API sur le resultat.
"""

from __future__ import annotations

from typing import Any

from app.dolibarr import DolibarrClient
from app.schemas.client import ClientContact, ClientDetail, ClientListResponse, ClientSummary
from app.schemas.common import PageMeta


def _to_summary(raw: dict[str, Any]) -> ClientSummary:
    return ClientSummary(
        id=str(raw.get("id")),
        name=raw.get("name") or raw.get("nom") or "",
        email=raw.get("email") or None,
        phone=raw.get("phone") or raw.get("phone_pro") or None,
        city=raw.get("town") or None,
        is_customer=str(raw.get("client", "0")) not in ("0", ""),
        is_supplier=str(raw.get("fournisseur", "0")) not in ("0", ""),
    )


def _to_detail(raw: dict[str, Any]) -> ClientDetail:
    summary = _to_summary(raw)
    contacts_raw = raw.get("contacts") or []
    contacts = [
        ClientContact(
            id=str(c.get("id")),
            full_name=" ".join(filter(None, [c.get("firstname"), c.get("lastname")])) or c.get("label", ""),
            phone=c.get("phone") or None,
            email=c.get("email") or None,
            role=c.get("civility") or None,
        )
        for c in contacts_raw
    ]
    extrafields = raw.get("array_options") or {}
    return ClientDetail(
        **summary.model_dump(),
        address=raw.get("address") or None,
        zip_code=raw.get("zip") or None,
        country=raw.get("country") or None,
        ninea=extrafields.get("options_ninea"),
        rccm=extrafields.get("options_rccm"),
        contacts=contacts,
    )


class ClientService:
    def __init__(self, dolibarr: DolibarrClient):
        self._dolibarr = dolibarr

    def search(self, query: str | None, page: int, limit: int) -> ClientListResponse:
        params: dict[str, Any] = {
            "limit": limit,
            "page": page - 1,  # l'API Dolibarr est paginee a partir de 0
            "sortfield": "t.nom",
            "sortorder": "ASC",
        }
        if query:
            # Recherche par nom (voir TODO en tete de fichier).
            escaped = query.replace("'", "")
            params["sqlfilters"] = f"(t.nom:like:'%{escaped}%')"

        raw_items = self._dolibarr.get("/thirdparties", params=params) or []

        if query:
            needle = query.lower()
            raw_items = [
                item
                for item in raw_items
                if needle in (item.get("name") or "").lower()
                or needle in (item.get("email") or "").lower()
                or needle in (item.get("phone") or "").lower()
                or needle in str(item.get("idprof1") or "").lower()  # reference / NINEA
            ]

        items = [_to_summary(item) for item in raw_items]
        return ClientListResponse(
            items=items,
            meta=PageMeta(page=page, limit=limit, has_more=len(items) == limit),
        )

    def get_by_id(self, client_id: str) -> ClientDetail:
        raw = self._dolibarr.get(f"/thirdparties/{client_id}", params={"includecontacts": 1})
        return _to_detail(raw)
