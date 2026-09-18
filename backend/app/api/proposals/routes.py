"""Module Devis — Sprint 2.

Volontairement non implemente en Sprint 1 (voir ARCHITECTURE.md, plan des
sprints). Router expose mais vide pour reserver le prefixe et permettre au
mobile de detecter la fonctionnalite a venir sans erreur 404 ambigue.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/proposals", tags=["proposals"])
