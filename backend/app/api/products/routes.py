from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import DolibarrDep
from app.dolibarr import DolibarrNotFoundError
from app.schemas.auth import CurrentUser
from app.schemas.product import ProductDetail, ProductListResponse
from app.security.dependencies import get_current_user
from app.security.rbac import require_permission, role_has_permission
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
def search_products(
    dolibarr: DolibarrDep,
    current_user: Annotated[CurrentUser, Depends(require_permission("products:read"))],
    query: str | None = Query(default=None, alias="query"),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
) -> ProductListResponse:
    include_margins = role_has_permission(
        current_user.role, "margins:view", override_margins=current_user.can_see_margins
    )
    return ProductService(dolibarr).search(
        query, category, page, limit, include_margins=include_margins
    )


@router.get("/{product_id}", response_model=ProductDetail)
def get_product(
    product_id: str,
    dolibarr: DolibarrDep,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> ProductDetail:
    if not role_has_permission(current_user.role, "products:read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acces refuse.")
    include_margins = role_has_permission(
        current_user.role, "margins:view", override_margins=current_user.can_see_margins
    )
    try:
        return ProductService(dolibarr).get_by_id(product_id, include_margins=include_margins)
    except DolibarrNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable.") from exc
