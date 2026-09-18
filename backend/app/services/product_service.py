"""Service catalogue produits/services (Dolibarr `/products`).

TODO(dolibarr-api): le filtrage par categorie metier (Solaire, Onduleurs,
Batteries, ...) suppose une correspondance entre les categories Dolibarr
configurees sur l'instance et les libelles du brief. A confirmer/mapper
avec l'equipe MG Assistance (id de categorie Dolibarr <-> libelle mobile)
avant le Sprint 2.
"""

from __future__ import annotations

from typing import Any

from app.dolibarr import DolibarrClient
from app.schemas.common import PageMeta
from app.schemas.product import ProductDetail, ProductListResponse, ProductSummary


def _to_summary(raw: dict[str, Any], *, include_margins: bool) -> ProductSummary:
    sale_price = _safe_float(raw.get("price"))
    purchase_price = _safe_float(raw.get("cost_price"))
    margin_amount = None
    margin_percent = None
    if include_margins and sale_price is not None and purchase_price is not None:
        margin_amount = round(sale_price - purchase_price, 2)
        if purchase_price:
            margin_percent = round((margin_amount / purchase_price) * 100, 2)

    return ProductSummary(
        id=str(raw.get("id")),
        ref=raw.get("ref") or "",
        label=raw.get("label") or "",
        category=None,  # TODO(dolibarr-api): resoudre via /products/{id}/categories
        stock=_safe_float(raw.get("stock_reel")),
        sale_price=sale_price,
        vat_rate=_safe_float(raw.get("tva_tx")),
        purchase_price=purchase_price if include_margins else None,
        margin_amount=margin_amount,
        margin_percent=margin_percent,
    )


def _safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class ProductService:
    def __init__(self, dolibarr: DolibarrClient):
        self._dolibarr = dolibarr

    def search(
        self, query: str | None, category: str | None, page: int, limit: int, *, include_margins: bool
    ) -> ProductListResponse:
        params: dict[str, Any] = {
            "limit": limit,
            "page": page - 1,
            "sortfield": "t.ref",
            "sortorder": "ASC",
        }
        if query:
            escaped = query.replace("'", "")
            params["sqlfilters"] = (
                f"(t.ref:like:'%{escaped}%') or (t.label:like:'%{escaped}%')"
            )

        raw_items = self._dolibarr.get("/products", params=params) or []
        items = [_to_summary(item, include_margins=include_margins) for item in raw_items]

        # TODO(dolibarr-api): filtre categorie applique cote MGA API en
        # attendant la resolution des ids de categorie (voir TODO en tete
        # de fichier) ; a deplacer dans `sqlfilters`/`category` cote
        # Dolibarr une fois le mapping confirme.
        if category:
            items = [i for i in items if (i.category or "").lower() == category.lower()]

        return ProductListResponse(
            items=items,
            meta=PageMeta(page=page, limit=limit, has_more=len(items) == limit),
        )

    def get_by_id(self, product_id: str, *, include_margins: bool) -> ProductDetail:
        raw = self._dolibarr.get(f"/products/{product_id}")
        summary = _to_summary(raw, include_margins=include_margins)
        return ProductDetail(
            **summary.model_dump(),
            description=raw.get("description") or None,
            unit=raw.get("fk_unit") or None,
            brand=None,  # TODO(dolibarr-api): extrafield marque a confirmer
        )
