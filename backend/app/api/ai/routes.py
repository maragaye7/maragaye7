"""Assistant MGA AI — Sprint 4.

Interface preparee uniquement (section 18 du brief : "Ne PAS encore
integrer un fournisseur IA reel. Preparer seulement les interfaces
necessaires."). Le workflow complet (comprendre -> extraire -> rechercher
dans Dolibarr -> proposer -> confirmer -> creer) sera implemente en Sprint 4,
avec la structure JSON `customer/items/commercial_parameters/missing_items/
warnings` decrite section 10 du brief. L'IA ne doit jamais valider
automatiquement un devis/commande/facture/paiement/suppression.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])
