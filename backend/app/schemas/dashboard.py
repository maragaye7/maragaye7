from typing import Literal

from pydantic import BaseModel

Period = Literal["today", "month", "year"]


class DashboardSummary(BaseModel):
    period: Period
    revenue: float
    proposals_pending: int
    proposals_accepted: int
    invoices_pending: int
    amount_to_collect: float
    active_orders: int
    active_projects: int
    currency: str = "FCFA"
