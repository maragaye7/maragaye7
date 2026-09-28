# Déploiement — MGA Mobile

Ce guide couvre le déploiement du **backend FastAPI** (`backend/`) et de
l'**application mobile Expo** (`mobile/`) du Sprint 1. Il complète
`README.md` (démarrage local) et `ARCHITECTURE.md` (conception).

---

## 1. Backend (MGA API — FastAPI)

### 1.1 Variables d'environnement (production)

Ne jamais committer de vraies valeurs. Définir ces variables sur la
plateforme d'hébergement (pas de fichier `.env` en prod) :

| Variable | Description |
|---|---|
| `APP_NAME` | Nom affiché, ex. `MGA API` |
| `ENVIRONMENT` | `production` |
| `DOLIBARR_BASE_URL` | `https://mgassistances.com/crm` |
| `DOLIBARR_API_URL` | `https://mgassistances.com/crm/api/index.php` |
| `DOLIBARR_API_KEY` | Clé API Dolibarr — **secret**, jamais loggée, jamais envoyée au mobile |
| `JWT_SECRET` | Secret long et aléatoire (ex. `openssl rand -hex 32`) — **différent** de la valeur de dev |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_MINUTES` | Durée de vie du token (ex. `60`) |
| `MGA_ADMIN_USERNAME` / `MGA_ADMIN_PASSWORD` | Identifiants du compte bootstrap Sprint 1 — à remplacer par de vrais comptes en base dès que possible |
| `CORS_ORIGINS` | Domaines autorisés, séparés par virgule (ex. `https://app.mgassistances.com`) — jamais `*` en prod |

### 1.2 Serveur applicatif

En développement, `uvicorn --reload` suffit. En production, utiliser un
process manager avec plusieurs workers, derrière un reverse proxy TLS :

```bash
cd backend
pip install -r requirements.txt
pip install gunicorn
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 --bind 0.0.0.0:8000
```

Placer un reverse proxy (Nginx, Caddy, ou le load balancer de la
plateforme choisie) devant, pour terminer le TLS (HTTPS obligatoire de
bout en bout, cf. `ARCHITECTURE.md` §8) et forwarder vers `127.0.0.1:8000`.

### 1.3 Options d'hébergement

Sans infrastructure existante, deux options simples pour un service
FastAPI + un seul process (pas de base de données requise en Sprint 1) :

**Option A — Render / Railway (PaaS, le plus rapide à mettre en place)**
1. Connecter le repo GitHub, sélectionner `backend/` comme répertoire racine.
2. Build command : `pip install -r requirements.txt`
3. Start command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Renseigner les variables d'environnement de la section 1.1 dans le
   dashboard de la plateforme (jamais dans le repo).
5. Noter l'URL HTTPS générée (ex. `https://mga-api.onrender.com`) — elle
   sera utilisée comme `EXPO_PUBLIC_API_URL` côté mobile.

**Option B — VPS (Docker)**

`backend/Dockerfile` (à ajouter si cette voie est retenue) :

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY app app
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "--bind", "0.0.0.0:8000"]
```

```bash
docker build -t mga-api ./backend
docker run -d --name mga-api --restart unless-stopped \
  --env-file backend/.env.production \
  -p 127.0.0.1:8000:8000 \
  mga-api
```

Puis configurer Nginx/Caddy pour le TLS et le reverse proxy vers
`127.0.0.1:8000`.

### 1.4 Vérification post-déploiement

```bash
curl https://<domaine-api>/health
# {"status":"ok","app":"MGA API"}
```

Tester ensuite `/auth/login` avec les identifiants configurés, puis un
endpoint protégé (`/dashboard`) avec le token obtenu.

---

## 2. Mobile (Expo / React Native)

### 2.1 Pointer vers l'API de production

Dans `mobile/.env` (jamais commité), remplacer l'URL locale par celle du
backend déployé :

```bash
EXPO_PUBLIC_API_URL=https://<domaine-api>
```

### 2.2 Test interne rapide (sans build natif)

Pour un test rapide avec l'app Expo Go, sans passer par les stores :

```bash
cd mobile
npm install
npx expo start
```

Partager le QR code / lien avec les testeurs (nécessite Expo Go installé
sur leur téléphone).

### 2.3 Build de production (EAS Build)

Pour une distribution réelle (TestFlight, Play Console interne, ou
installation directe), utiliser EAS Build :

```bash
cd mobile
npm install -g eas-cli
eas login
eas build:configure
```

Cela crée `eas.json`. Définir un profil `production` qui embarque
`EXPO_PUBLIC_API_URL` pointant vers l'API de production (via
`eas.json` → `build.production.env`, ou des secrets EAS si l'URL doit
rester privée).

```bash
eas build --platform android --profile production
eas build --platform ios --profile production
```

Distribution :
- **Android** : APK/AAB téléchargeable directement, ou envoi vers Google
  Play Console (interne/production).
- **iOS** : nécessite un compte Apple Developer ; `eas submit` pour
  pousser vers TestFlight/App Store.

### 2.4 Points d'attention

- `app.json` définit `slug: "mga-mobile"` et `scheme: "mgamobile"` —
  garder cette valeur stable entre les builds (identifie l'app pour EAS).
- `expo-secure-store` est utilisé pour stocker le token JWT ; aucune
  configuration native supplémentaire n'est requise, mais vérifier que le
  plugin reste listé dans `app.json` → `plugins`.
- Ne jamais mettre `DOLIBARR_API_KEY` ou tout secret backend dans une
  variable `EXPO_PUBLIC_*` : ces valeurs sont embarquées en clair dans le
  bundle de l'app et visibles par quiconque l'inspecte.

---

## 3. Checklist avant mise en production

- [ ] `JWT_SECRET` régénéré (différent de la valeur `.env.example`)
- [ ] `MGA_ADMIN_PASSWORD` changé, ou compte bootstrap remplacé par de
      vrais comptes utilisateurs (cf. `ARCHITECTURE.md` §3.1, Sprint 2)
- [ ] `CORS_ORIGINS` limité aux domaines réels du mobile/web, pas de `*`
- [ ] `DOLIBARR_API_KEY` renseignée uniquement côté serveur (jamais dans
      le mobile ni dans Git)
- [ ] HTTPS actif sur l'API (certificat valide, pas de contenu mixte)
- [ ] `EXPO_PUBLIC_API_URL` du build mobile pointe vers l'URL HTTPS de
      production, pas `127.0.0.1` ni une IP locale
- [ ] `GET /health` répond `200` depuis l'extérieur du réseau
      d'hébergement
