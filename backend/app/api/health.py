"""Endpoints de sante / diagnostic.

`/health/dolibarr` sert de test de connexion Dolibarr (section 18.6 du
brief). TODO(dolibarr-api): confirmer sur l'instance reelle l'endpoint le
plus leger pour un ping (ex. `/status` s'il existe sur Dolibarr 23, sinon
repli sur un GET `/thirdparties` limite a 1 resultat, deja utilise ici).
"""

from fastapi import APIRouter

from app.api.deps import DolibarrDep
from app.dolibarr import DolibarrClientError
from app.schemas.common import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
def health() -> HealthStatus:
    return HealthStatus(status="ok")


@router.get("/health/dolibarr", response_model=HealthStatus)
def health_dolibarr(dolibarr: DolibarrDep) -> HealthStatus:
    try:
        dolibarr.get("/thirdparties", params={"limit": 1})
    except DolibarrClientError as exc:
        return HealthStatus(status="error", detail=str(exc))
    return HealthStatus(status="ok", detail="Connexion Dolibarr operationnelle.")
