# MGA Mobile — Architecture (Livrable Sprint 0)

Ce document est le livrable demandé avant l'écriture du code (section 20 du brief).
Il couvre : architecture finale, arborescence, modèle de données, stratégie
d'authentification, endpoints MGA API, mapping MGA API ↔ Dolibarr, stratégie
offline, sécurité, plan de tests, plan des sprints.

Le code du **Sprint 1** (section 18 du brief) a été développé dans ce même
commit, dans `backend/` et `mobile/`.

Le déploiement (Docker Compose + Alembic pour le backend, EAS Build/Submit
pour le mobile) est documenté dans `DEPLOYMENT.md` et
`MOBILE_DEPLOYMENT.md`.

---

## 1. Architecture finale proposée

Trois composants indépendants, déployables séparément :

```
┌────────────────────┐        HTTPS/JWT        ┌────────────────────┐        HTTPS/DOLAPIKEY        ┌────────────────────┐
│   MGA Mobile App    │ ───────────────────────▶│      MGA API        │ ──────────────────────────────▶│  Dolibarr 23 (CRM)  │
│  React Native/Expo  │◀─────────────────────── │  FastAPI + Postgres │◀────────────────────────────── │  mgassistances.com  │
└────────────────────┘                          └────────────────────┘                                └────────────────────┘
```

Principes directeurs :

- **Dolibarr reste la source de vérité** pour toutes les données métier
  (tiers, produits, devis, commandes, factures, projets). MGA API ne
  duplique jamais ces données en base — elle les relaie et les met en
  forme.
- **PostgreSQL (MGA API)** ne stocke que ce qui n'existe pas dans Dolibarr :
  comptes utilisateurs mobiles (RBAC applicatif), tokens de rafraîchissement,
  file d'attente offline (idempotence), logs d'audit, préférences.
- **Le mobile ne connaît jamais `DOLAPIKEY`**. Il ne parle qu'à MGA API,
  authentifié par JWT.
- Aucun accès direct à MySQL Dolibarr : tout passe par l'API REST
  `https://mgassistances.com/crm/api/index.php`.

---

## 2. Arborescence du repository

```
maragaye7/
├── ARCHITECTURE.md
├── README.md
├── backend/                     # MGA API (FastAPI)
│   ├── app/
│   │   ├── main.py
│   │   ├── config/               # Settings (pydantic-settings), variables d'env
│   │   ├── api/                  # Routers HTTP, un sous-package par domaine
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── clients/
│   │   │   ├── products/
│   │   │   ├── proposals/        # stub Sprint 2
│   │   │   ├── invoices/         # stub Sprint 2
│   │   │   ├── orders/           # stub Sprint 2
│   │   │   ├── projects/         # stub Sprint 2
│   │   │   ├── ai/               # interface seulement (pas de provider réel)
│   │   │   └── solar/            # interface seulement (pas de calculs réels)
│   │   ├── dolibarr/             # DolibarrClient centralisé + exceptions
│   │   ├── services/             # logique métier, appelle dolibarr/ et models/
│   │   ├── models/               # SQLAlchemy (DB locale MGA : User, RefreshToken, ...)
│   │   ├── schemas/               # Pydantic (contrats API MGA)
│   │   ├── security/              # JWT, hash mots de passe, RBAC
│   │   └── database/              # session SQLAlchemy, base declarative
│   ├── tests/                    # pytest, tout appel Dolibarr est mocké
│   ├── requirements.txt
│   └── .env.example
└── mobile/                       # MGA Mobile (Expo / React Native / TypeScript)
    ├── app/                       # Expo Router (fichiers = routes)
    │   ├── login/
    │   └── (app)/                 # groupe protégé par auth
    │       ├── dashboard/
    │       ├── clients/
    │       ├── products/
    │       └── settings/
    ├── components/                # MGACard, MGAButton, MGAInput, MGAMoney, ...
    ├── services/                  # client HTTP MGA API (axios + intercepteurs)
    ├── hooks/                     # hooks TanStack Query par domaine
    ├── stores/                    # Zustand (état auth, préférences)
    ├── types/                     # types TypeScript partagés
    ├── utils/                     # formatage FCFA, thème, helpers
    ├── app.json
    ├── package.json
    └── .env.example
```

---

## 3. Modèle de données

### 3.1 Base PostgreSQL de MGA API (locale, pas Dolibarr)

MGA API ne réplique pas les objets métier Dolibarr. Elle stocke uniquement :

**`users`** (comptes mobiles, distincts des utilisateurs internes Dolibarr) :

| champ              | type      | notes                                            |
|--------------------|-----------|---------------------------------------------------|
| id                 | UUID      | PK                                                 |
| email              | string    | unique                                             |
| hashed_password    | string    | bcrypt                                             |
| full_name          | string    |                                                     |
| role               | enum      | ADMIN, DIRECTION, COMMERCIAL, TECHNICIEN           |
| dolibarr_user_id   | int, null | id de l'utilisateur Dolibarr correspondant (optionnel, pour audit) |
| is_active          | bool      |                                                     |
| can_see_margins    | bool      | override ponctuel du défaut RBAC                  |
| created_at / updated_at | datetime |                                               |

**`refresh_tokens`** : id, user_id (FK), token_hash, expires_at, revoked_at, device_info.

**`audit_logs`** : id, user_id, action, resource_type, resource_id (id Dolibarr concerné),
payload_summary (jamais de données sensibles), created_at.

**`offline_operations`** (Sprint 3+, cf. §7) : id, idempotency_key (unique),
user_id, operation_type (ex. `create_proposal`), payload_json, status
(PENDING/SYNCING/DONE/FAILED), dolibarr_object_id (une fois créé), created_at,
synced_at.

Ces tables sont gérées par SQLAlchemy ; migrations Alembic à introduire dès
que le schéma se stabilise (TODO Sprint 2 — en Sprint 1 `create_all` suffit
en développement).

### 3.2 Objets Dolibarr consommés (lecture/écriture via API REST, jamais stockés)

- **Thirdparty** (tiers/clients) — `/thirdparties`
- **Contact** — `/contacts`
- **Product** (produits/services) — `/products`
- **Propal** (devis) — `/proposals`
- **Order** (commande) — `/orders`
- **Invoice** (facture) — `/invoices`
- **Project** (projet/chantier) — `/projects`
- **Document** (PDF générés) — `/documents`

Les schémas Pydantic MGA (`app/schemas/`) sont des **DTOs volontairement plus
simples** que les objets Dolibarr bruts : ils exposent uniquement les champs
utiles au mobile, avec des noms stables, indépendants des évolutions internes
de Dolibarr.

---

## 4. Stratégie d'authentification

Double niveau, comme prévu par l'architecture :

1. **Mobile ↔ MGA API** : JWT applicatif.
   - `POST /auth/login` (email + mot de passe du compte MGA local) →
     `access_token` (courte durée, 15 min) + `refresh_token` (longue durée,
     30 jours, stocké hashé en base, révocable).
   - `POST /auth/refresh` → nouveau couple de tokens (rotation du refresh
     token : l'ancien est révoqué).
   - `POST /auth/logout` → révoque le refresh token courant.
   - Stockage mobile : `expo-secure-store` (Keychain iOS / Keystore Android),
     jamais `AsyncStorage` en clair.
   - Biométrie (Face ID / Touch ID / empreinte Android) : prévue en Sprint
     ultérieur via `expo-local-authentication`, déverrouille l'accès au
     refresh token déjà stocké — ne remplace pas le login initial.

2. **MGA API ↔ Dolibarr** : `DOLAPIKEY` (clé API technique unique, configurée
   côté serveur uniquement via variable d'environnement), envoyée dans le
   header `DOLAPIKEY` par `DolibarrClient`. Le mobile n'y a jamais accès.

### RBAC

| Rôle        | Dashboard | Clients | Produits | Devis | Commandes | Factures | Projets | Prix d'achat / Marges |
|-------------|:---------:|:-------:|:--------:|:-----:|:---------:|:--------:|:-------:|:----------------------:|
| ADMIN       | ✔ complet | ✔ CRUD  | ✔ CRUD   | ✔ CRUD| ✔ CRUD    | ✔ CRUD   | ✔ CRUD  | ✔ visible              |
| DIRECTION   | ✔ CA/marges | ✔ lecture | ✔ lecture | ✔ lecture | ✔ lecture | ✔ lecture | ✔ lecture | ✔ visible          |
| COMMERCIAL  | ✔ limité  | ✔ CRUD  | ✔ lecture | ✔ CRUD | ✔ CRUD   | ✔ lecture| ✘       | ✘ masqué par défaut    |
| TECHNICIEN  | ✘         | ✔ lecture | ✔ lecture (sans prix achat) | ✘ | ✘ | ✘ | ✔ CRUD (interventions, photos) | ✘ masqué |

Implémentation : dépendance FastAPI `require_role(*roles)` +
`require_permission("margins:view")`, vérifiée à la fois sur les routes et
dans la sérialisation des schémas (un champ `purchase_price` /
`margin_amount` est retiré de la réponse si l'appelant n'a pas la permission,
jamais seulement caché côté mobile).

---

## 5. Endpoints MGA API (Sprint 1)

Base : `/api/v1`

**Auth**
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET  /auth/me`

**Dashboard**
- `GET /dashboard/summary?period=today|month|year`

**Clients**
- `GET  /clients?query=&page=&limit=`
- `GET  /clients/{id}`
- `POST /clients` *(Sprint 2 : écriture réelle vers Dolibarr, confirmation obligatoire)*
- `PUT  /clients/{id}` *(Sprint 2)*

**Produits**
- `GET /products?query=&category=&page=&limit=`
- `GET /products/{id}`

**Santé / diagnostic**
- `GET /health`
- `GET /health/dolibarr` (test de connexion Dolibarr, section 18.6)

Endpoints Sprint 2+ (stubs créés, non implémentés) : `/proposals`,
`/orders`, `/invoices`, `/projects`, `/ai/*`, `/solar/*`.

---

## 6. Mapping MGA API ↔ Dolibarr

| MGA API                     | Méthode Dolibarr REST                          | Notes |
|------------------------------|------------------------------------------------|-------|
| `GET /clients`               | `GET /thirdparties?sqlfilters=...&limit=&page=`| recherche nom/email/tél via `sqlfilters` (TODO Sprint 2 : valider la syntaxe exacte des filtres combinés sur l'instance 23 réelle) |
| `GET /clients/{id}`          | `GET /thirdparties/{id}`                       | inclut contacts si `includecontacts=1` (TODO : vérifier support sur v23) |
| `GET /products`              | `GET /products?sqlfilters=&limit=&page=`       | catégorie via `/products/{id}/categories` ou filtre `fk_category` (TODO à confirmer) |
| `GET /products/{id}`         | `GET /products/{id}`                           | |
| `POST /clients` (Sprint 2)   | `POST /thirdparties`                            | écran de confirmation obligatoire avant appel |
| `POST /proposals` (Sprint 2+)| `POST /proposals` puis `PUT /proposals/{id}/lines`| workflow multi-appels, idempotence requise |
| `GET /documents/{id}.pdf`    | `GET /documents/download?modulepart=...`        | TODO Sprint 2 : confirmer paramètres exacts sur v23 |
| `GET /health/dolibarr`       | `GET /status` ou `GET /login` (selon dispo)     | TODO : confirmer l'endpoint de test de connexion le plus léger sur l'instance cible |

Toute case marquée **TODO** est documentée comme telle dans le code
(`# TODO(dolibarr-api): ...`) plutôt que devinée, conformément à la règle du
brief : ne jamais inventer le comportement d'un endpoint incertain. La
validation se fera contre l'instance réelle `https://mgassistances.com/crm`
dès qu'un accès de test sera disponible.

---

## 7. Stratégie offline

Approche en trois couches, dont seule la première est livrée en Sprint 1 :

1. **Cache de lecture** (TanStack Query + `persistQueryClient` sur
   AsyncStorage) : clients récents, catalogue produits, devis brouillons,
   projets récents restent consultables hors ligne. Sprint 1 : mise en place
   de l'infrastructure TanStack Query (staleTime, cache time) ; persistance
   effective en Sprint 2.
2. **File d'attente d'écriture** : toute mutation (création devis, client…)
   effectuée hors ligne est stockée localement (table `offline_operations`
   décrite en §3.1, miroir léger côté mobile via SQLite/AsyncStorage) avec un
   statut visible : `Hors ligne` / `Synchronisation en attente` / `Synchronisé`.
3. **Idempotence côté backend** : chaque opération d'écriture envoyée par le
   mobile porte une **clé d'idempotence** (UUID généré à la création locale
   de l'objet, avant toute tentative réseau). MGA API vérifie cette clé dans
   `offline_operations` avant de relayer vers Dolibarr : une clé déjà
   traitée renvoie le résultat existant sans recréer l'objet. Cela garantit
   qu'un devis n'est jamais créé deux fois lors d'une reprise de
   synchronisation.

Cette stratégie est **préparée** en Sprint 1 (schéma de données, champ
`idempotency_key` sur les endpoints d'écriture futurs) mais l'implémentation
complète (queue mobile, retry automatique, résolution de conflits) est
planifiée Sprint 3, une fois les modules d'écriture (devis, commandes)
disponibles.

---

## 8. Sécurité

- **HTTPS obligatoire** de bout en bout (mobile → MGA API → Dolibarr).
- **JWT** signés (HS256 en dev, RS256 recommandé en prod), courte durée de
  vie pour l'access token, rotation du refresh token.
- **RBAC** appliqué côté serveur (jamais seulement côté UI).
- **Validation stricte** de toutes les entrées via Pydantic (schémas
  distincts *input*/*output*).
- **Rate limiting** sur `/auth/login` et endpoints sensibles (slowapi /
  middleware dédié — TODO Sprint 2, dépendance à ajouter).
- **CORS restrictif** : origines explicitement listées via variable d'env,
  pas de wildcard en production.
- **Timeouts et retry contrôlé** sur `DolibarrClient` (timeout 10s par
  défaut, retry limité aux erreurs réseau/5xx, jamais sur les écritures non
  idempotentes sans clé d'idempotence).
- **Logs & audit trail** : `audit_logs` pour toute action sensible (login,
  création/modification d'objets métier) ; logs applicatifs structurés.
- **Secrets** : `DOLAPIKEY`, mots de passe, tokens JWT (access/refresh) ne
  sont **jamais loggés** — un filtre de log dédié masque ces champs. Aucun
  secret réel n'est commité (`.env.example` fournis, `.env` dans
  `.gitignore`).
- **Aucun accès direct MySQL Dolibarr.**

---

## 9. Plan de tests

Backend (pytest, `backend/tests/`) :

- `test_dolibarr_client.py` : succès, erreur HTTP (4xx/5xx), timeout,
  format de réponse inattendu — **`DolibarrClient` entièrement mocké**,
  aucun appel réseau réel.
- `test_auth.py` : login valide/invalide, refresh, expiration, logout,
  vérification RBAC (accès refusé pour un rôle non autorisé).
- `test_clients.py` : recherche client (nom/email/téléphone/référence),
  pagination, permissions sur les champs marge/prix d'achat.
- `test_products.py` : recherche produit (référence/désignation/catégorie),
  pagination, masquage des prix d'achat pour TECHNICIEN/COMMERCIAL.
- `test_health.py` : `/health` et `/health/dolibarr` (mocké).

Toutes les mutations (`POST`/`PUT`/`DELETE`) sont testées contre un
`DolibarrClient` mocké — **aucune modification réelle de l'instance Dolibarr
de production** pendant les tests.

Mobile (Sprint 2+) : tests de composants (Jest + Testing Library) sur les
composants `MGA*`, tests d'intégration des écrans critiques (login,
recherche client), tests E2E ciblés (Maestro/Detox) sur le parcours devis
une fois ce module livré.

---

## 10. Plan des sprints

**Sprint 0 (ce livrable)** — architecture, arborescence, environnement.

**Sprint 1 (livré dans ce commit)**
1. Structure du repository (backend + mobile).
2. Configuration environnement (`.env.example`, settings typées).
3. Backend FastAPI (squelette, routers, `main.py`).
4. `DolibarrClient` (GET/POST/PUT/DELETE, timeout, retry, logs sécurisés).
5. Authentification MGA (JWT + RBAC + comptes locaux).
6. `/health/dolibarr` — test de connexion Dolibarr.
7. Récupération des clients (`/clients`, recherche, pagination).
8. Récupération des produits (`/products`, recherche, pagination).
9. Écran mobile Login.
10. Dashboard mobile initial (structure + actions rapides, données mockées
    tant que `/dashboard/summary` n'agrège pas encore tous les indicateurs
    Dolibarr réels).
11. Écran mobile Liste clients.
12. Écran mobile Fiche client.
13. Écran mobile Catalogue produits.

**Sprint 2**
- Écriture Dolibarr (création/modification client) avec écran de
  confirmation.
- Module Devis (lecture + création, écran de récapitulatif obligatoire
  avant validation).
- Documents PDF (visualisation, téléchargement, partage).
- Persistance offline en lecture (cache TanStack Query).
- Alembic pour les migrations DB.

**Sprint 3**
- Commandes, Factures (lecture puis transformation devis→commande→facture,
  toujours avec confirmation utilisateur).
- File d'attente offline en écriture + idempotence complète.
- Projets/chantiers, photos de chantier.
- Rate limiting, durcissement sécurité.

**Sprint 4**
- Assistant MGA AI (workflow décrit section 10 du brief : extraction →
  recherche produits réels → proposition → confirmation → création devis
  uniquement après validation humaine).
- Biométrie mobile.

**Sprint 5+**
- Dimensionnement solaire (Solar Design) : saisie consommation, calculs
  PV/onduleur/stockage, génération BOM → prix Dolibarr → devis.
- Analyse financière (ROI, cash-flow, économies 25 ans).

Chaque sprint suit la règle du brief : vérifier la documentation/l'endpoint
Dolibarr réel avant d'intégrer, créer types/schémas, service, tests, puis
seulement l'interface mobile.
