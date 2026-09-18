"""Dimensionnement solaire (Solar Design) — Sprint 5+.

Non developpe en Sprint 1, conformement au brief. Architecture des futures
entrees/calculs/sorties documentee dans ARCHITECTURE.md et section 11 du
brief (DIMENSIONNEMENT -> BOM -> PRIX DOLIBARR -> DEVIS).
"""

from fastapi import APIRouter

router = APIRouter(prefix="/solar", tags=["solar"])
