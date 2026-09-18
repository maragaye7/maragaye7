from fastapi import APIRouter

from app.api import health
from app.api.ai.routes import router as ai_router
from app.api.auth.routes import router as auth_router
from app.api.clients.routes import router as clients_router
from app.api.dashboard.routes import router as dashboard_router
from app.api.invoices.routes import router as invoices_router
from app.api.orders.routes import router as orders_router
from app.api.products.routes import router as products_router
from app.api.projects.routes import router as projects_router
from app.api.proposals.routes import router as proposals_router
from app.api.solar.routes import router as solar_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(clients_router)
api_router.include_router(products_router)

# Sprints suivants : routers exposes mais sans endpoints tant que le
# module n'est pas developpe (voir ARCHITECTURE.md, plan des sprints).
api_router.include_router(proposals_router)
api_router.include_router(invoices_router)
api_router.include_router(orders_router)
api_router.include_router(projects_router)
api_router.include_router(ai_router)
api_router.include_router(solar_router)
