from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import DolibarrDep
from app.dolibarr import DolibarrNotFoundError
from app.schemas.auth import CurrentUser
from app.schemas.client import ClientDetail, ClientListResponse
from app.security.rbac import require_permission
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=ClientListResponse)
def search_clients(
    dolibarr: DolibarrDep,
    current_user: Annotated[CurrentUser, Depends(require_permission("clients:read"))],
    query: str | None = Query(default=None, alias="query"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
) -> ClientListResponse:
    return ClientService(dolibarr).search(query, page, limit)


@router.get("/{client_id}", response_model=ClientDetail)
def get_client(
    client_id: str,
    dolibarr: DolibarrDep,
    current_user: Annotated[CurrentUser, Depends(require_permission("clients:read"))],
) -> ClientDetail:
    try:
        return ClientService(dolibarr).get_by_id(client_id)
    except DolibarrNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client introuvable.") from exc
