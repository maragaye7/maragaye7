# MGA Mobile — Sprint 1

Application mobile MG Assistance connectée à Dolibarr 23 via un backend FastAPI sécurisé.

## Structure
- `backend/` : FastAPI, JWT, client Dolibarr, endpoints Dashboard/Clients/Produits
- `mobile/` : Expo + React Native + TypeScript, écrans Login/Dashboard/Clients/Produits

## Sécurité
La `DOLIBARR_API_KEY` reste uniquement dans `backend/.env`. Ne jamais la mettre dans l'application mobile ni dans Git.

## Démarrage backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Renseigner DOLIBARR_API_KEY et changer JWT_SECRET
uvicorn app.main:app --reload --port 8000
```

Tests rapides :
- `GET http://localhost:8000/health`
- Swagger : `http://localhost:8000/docs`

## Démarrage mobile
```bash
cd mobile
npm install
cp .env.example .env
npm run start
```

Pour tester sur un téléphone physique, `EXPO_PUBLIC_API_URL` doit pointer vers l'IP LAN de l'ordinateur, par exemple `http://192.168.1.20:8000`.

## Déploiement

Voir [`DEPLOYMENT.md`](./DEPLOYMENT.md) pour déployer le backend en
production (Render/Railway/Docker) et distribuer l'app mobile (EAS Build).

## Sprint 1
1. Login MGA
2. Dashboard
3. Clients Dolibarr
4. Produits Dolibarr

Les écritures Dolibarr (devis/factures) sont volontairement exclues de ce sprint.
