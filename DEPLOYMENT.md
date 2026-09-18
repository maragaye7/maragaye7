# Déploiement — MGA API (backend)

Ce guide déploie le backend FastAPI (`backend/`) sur un VPS avec Docker
Compose : API + PostgreSQL + Caddy (reverse proxy HTTPS automatique via
Let's Encrypt). Voir `ARCHITECTURE.md` pour le contexte général.

Le déploiement de l'app mobile est documenté séparément dans
`MOBILE_DEPLOYMENT.md`.

## 1. Prérequis sur le VPS

- Un VPS Linux (Ubuntu 22.04/24.04 recommandé) avec au moins 1 vCPU / 1 Go
  de RAM.
- Docker Engine + le plugin Docker Compose installés :
  ```bash
  curl -fsSL https://get.docker.com | sh
  ```
- Un sous-domaine pointant vers l'IP du VPS, par exemple
  `api.mgassistances.com` (enregistrement DNS de type A). Caddy a besoin
  que ce DNS soit déjà résolu pour obtenir automatiquement le certificat
  Let's Encrypt.
- Les ports **80** et **443** ouverts (pare-feu / groupe de sécurité).

## 2. Récupérer le code

```bash
git clone https://github.com/maragaye7/maragaye7.git
cd maragaye7/deploy
```

## 3. Configurer les secrets

```bash
cp .env.example .env
```

Éditer `.env` et renseigner (voir `deploy/.env.example` pour la liste
complète) :

- `API_DOMAIN` : le sous-domaine DNS pointant vers ce VPS.
- `POSTGRES_PASSWORD` : mot de passe fort pour la base locale MGA.
- `DOLIBARR_API_KEY` : la vraie clé API Dolibarr (`DOLAPIKEY`), obtenue
  dans Dolibarr → Configuration → Modules → API/Web services → clé de
  l'utilisateur technique dédié. **Ne jamais commiter ce fichier** (il est
  dans `.gitignore`).
- `JWT_SECRET_KEY` : une valeur aléatoire d'au moins 32 caractères, par
  exemple `openssl rand -hex 32`.
- `CORS_ALLOWED_ORIGINS` : origines autorisées pour l'app mobile en
  production (pas de wildcard `*`).

## 4. Démarrer la stack

```bash
docker compose up -d --build
```

Au démarrage, le conteneur `api` exécute automatiquement
`alembic upgrade head` (voir `backend/docker-entrypoint.sh`) avant de
lancer le serveur : le schéma PostgreSQL est toujours à jour avant que du
trafic ne soit servi. Caddy demande et renouvelle seul le certificat TLS
pour `API_DOMAIN`.

Vérifier que tout est démarré :

```bash
docker compose ps
curl -s https://api.mgassistances.com/api/v1/health
curl -s https://api.mgassistances.com/api/v1/health/dolibarr
```

`health/dolibarr` confirme que la connexion à
`https://mgassistances.com/crm` fonctionne avec la clé API configurée.

## 5. Créer le premier compte administrateur

Sprint 1 ne fournit pas encore d'écran d'inscription (volontairement : les
comptes MGA Mobile sont créés par un administrateur, pas en libre-service).
Créer le premier compte ADMIN directement en base :

```bash
docker compose exec api python -c "
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.security.password import hash_password

db = SessionLocal()
db.add(User(
    email='admin@mgassistances.com',
    hashed_password=hash_password('CHANGE_ME'),
    full_name='Administrateur MGA',
    role=UserRole.ADMIN,
    can_see_margins=True,
))
db.commit()
"
```

Changer immédiatement ce mot de passe après la première connexion (pas
d'écran dédié en Sprint 1 : mettre à jour `hashed_password` via le même
mécanisme, ou attendre l'écran de gestion des comptes prévu en Sprint 2).

## 6. Mises à jour

```bash
cd maragaye7
git pull
cd deploy
docker compose up -d --build
```

Les migrations Alembic en attente sont appliquées automatiquement au
redémarrage du conteneur `api`.

## 7. Sauvegardes

La base PostgreSQL vit dans le volume Docker `deploy_db_data`. Sauvegarde
minimale recommandée (cron quotidien sur le VPS) :

```bash
docker compose exec -T db pg_dump -U mga mga_api | gzip > backup-$(date +%F).sql.gz
```

Dolibarr reste la source de vérité pour les données métier (clients,
produits, devis...) : cette base ne contient que les comptes MGA Mobile et
les refresh tokens, donc une perte n'affecte pas les données ERP.

## 8. CI

`.github/workflows/backend-ci.yml` fait tourner la suite de tests (tous
les appels Dolibarr mockés, voir `backend/tests/`) et vérifie qu'aucune
migration Alembic n'a été oubliée (`alembic check` contre un vrai
PostgreSQL de CI) à chaque push/PR touchant `backend/`.

## 9. Limites connues de ce premier déploiement

- Pas encore de CD automatique (déploiement déclenché manuellement via SSH
  sur le VPS). Une CD GitHub Actions (build + push d'image + SSH deploy)
  pourra être ajoutée une fois un VPS cible et ses secrets disponibles.
- Pas de haute disponibilité (une seule instance API, une seule instance
  PostgreSQL) : suffisant pour ce stade du projet, à revoir si la charge
  augmente.
- Le premier compte admin se crée manuellement (pas d'écran d'inscription,
  volontairement — voir section 5).
