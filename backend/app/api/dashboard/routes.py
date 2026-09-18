from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DolibarrDep
from app.schemas.auth import CurrentUser
from app.schemas.dashboard import DashboardSummary, Period
from app.security.rbac import require_permission
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    dolibarr: DolibarrDep,
    current_user: Annotated[CurrentUser, Depends(require_permission("dashboard:view"))],
    period: Period = "month",
) -> DashboardSummary:
    return DashboardService(dolibarr).get_summary(period)
