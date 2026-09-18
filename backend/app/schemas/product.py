from pydantic import BaseModel

from app.schemas.common import PageMeta


class ProductSummary(BaseModel):
    """Vue allegee d'un produit/service Dolibarr, pour les listes du catalogue."""

    id: str
    ref: str
    label: str
    category: str | None = None
    stock: float | None = None
    sale_price: float | None = None
    vat_rate: float | None = None

    # Visibles uniquement si l'appelant a la permission "margins:view"
    # (retires de la reponse serveur, jamais seulement caches cote mobile).
    purchase_price: float | None = None
    margin_amount: float | None = None
    margin_percent: float | None = None


class ProductDetail(ProductSummary):
    description: str | None = None
    unit: str | None = None
    brand: str | None = None


class ProductListResponse(BaseModel):
    items: list[ProductSummary]
    meta: PageMeta
