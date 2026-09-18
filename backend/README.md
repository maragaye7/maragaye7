# MGA API (backend)

Backend FastAPI servant d'intermediaire entre MGA Mobile et Dolibarr.
Voir `../ARCHITECTURE.md` pour l'architecture complete.

## Installation locale

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # puis renseigner les vraies valeurs (jamais commit .env)
```

## Lancer le serveur

```bash
uvicorn app.main:app --reload
```

La documentation interactive est disponible sur `/docs` une fois le
serveur lance.

## Lancer les tests

```bash
pytest
```

Tous les appels Dolibarr sont mockes dans les tests (aucune requete reelle
vers `https://mgassistances.com/crm`).
