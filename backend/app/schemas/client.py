from pydantic import BaseModel

from app.schemas.common import PageMeta


class ClientContact(BaseModel):
    id: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    role: str | None = None


class ClientSummary(BaseModel):
    """Vue allegee d'un tiers Dolibarr, pour les listes."""

    id: str
    name: str
    email: str | None = None
    phone: str | None = None
    city: str | None = None
    is_customer: bool = True
    is_supplier: bool = False


class ClientDetail(ClientSummary):
    """Fiche client complete, mappee depuis un `Thirdparty` Dolibarr."""

    address: str | None = None
    zip_code: str | None = None
    country: str | None = None
    ninea: str | None = None  # extrafield Dolibarr (TODO Sprint 2: confirmer le code exact)
    rccm: str | None = None  # extrafield Dolibarr (TODO Sprint 2: confirmer le code exact)
    contacts: list[ClientContact] = []


class ClientListResponse(BaseModel):
    items: list[ClientSummary]
    meta: PageMeta
