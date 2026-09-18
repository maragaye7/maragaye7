"""Service d'agregation du tableau de bord.

TODO(dolibarr-api): l'agregation reelle du CA, des devis en cours/acceptes,
factures en attente, etc. necessite plusieurs appels Dolibarr (`/proposals`,
`/invoices`, `/orders`, ou des endpoints de statistiques s'ils existent sur
la v23). Ce Sprint 1 fournit la structure de reponse et un calcul minimal ;
le calcul complet sera branche au Sprint 2 quand les modules devis/factures
seront integres, en suivant la regle "verifier avant d'integrer".
"""

from __future__ import annotations

from app.dolibarr import DolibarrClient
from app.schemas.dashboard import DashboardSummary, Period


class DashboardService:
    def __init__(self, dolibarr: DolibarrClient):
        self._dolibarr = dolibarr

    def get_summary(self, period: Period) -> DashboardSummary:
        # Placeholder Sprint 1 : structure stable pour le mobile, valeurs a
        # 0 tant que les modules devis/commandes/factures ne sont pas
        # integres (voir plan des sprints, ARCHITECTURE.md section 10).
        return DashboardSummary(
            period=period,
            revenue=0,
            proposals_pending=0,
            proposals_accepted=0,
            invoices_pending=0,
            amount_to_collect=0,
            active_orders=0,
            active_projects=0,
        )
