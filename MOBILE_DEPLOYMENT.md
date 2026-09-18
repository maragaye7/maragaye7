# Déploiement — MGA Mobile (Expo / App Store & Play Store)

Ce guide construit et publie `mobile/` sur l'App Store (iOS) et le Play
Store (Android) via EAS Build/Submit. Contrairement au backend, ces étapes
ne peuvent pas être exécutées par un agent automatisé : elles nécessitent
tes propres comptes développeur Apple/Google et une session interactive
(`eas login`, validations 2FA Apple, etc.). Ce document est donc un
**runbook** à suivre toi-même (ou à donner à qui s'en charge).

## 0. Ce qui a déjà été préparé dans le repo

- `mobile/eas.json` : profils de build `development` / `preview` /
  `production`, et profil de soumission `production` (App Store Connect +
  Google Play) avec des valeurs `CHANGE_ME_*` à remplacer.
- `mobile/app.json` : `ios.bundleIdentifier` / `android.package`
  (`sn.mgassistance.mgamobile`), `ios.buildNumber` / `android.versionCode`
  initialisés à `1`, `extra.eas.projectId` à remplacer une fois le projet
  EAS créé.
- `mobile/assets/icon.png`, `adaptive-icon.png`, `favicon.png`,
  `splash-icon.png` : **placeholders générés automatiquement** (fond vert
  MG Assistance, texte "MGA") pour que la config soit immédiatement
  buildable. **À remplacer par les vrais visuels de marque MG Assistance**
  avant toute soumission aux stores (Apple/Google rejettent les icônes
  non définitives). Spécifications :
  - `icon.png` : 1024×1024, sans transparence, sans coins arrondis
    (Apple applique le masque lui-même).
  - `adaptive-icon.png` : 1024×1024, sujet centré dans le cercle de sécurité
    central (~66% de la surface), fond transparent.
  - `splash-icon.png` : logo seul sur fond transparent/uni, affiché centré
    par Expo au démarrage.

## 1. Comptes requis

- **Compte Expo** (gratuit) : https://expo.dev/signup — pour EAS
  Build/Submit et l'OTA update (channels `preview`/`production`).
- **Apple Developer Program** (99 $/an) : https://developer.apple.com —
  nécessaire pour publier sur l'App Store et obtenir les certificats de
  signature iOS.
- **Google Play Console** (25 $ à vie) : https://play.google.com/console —
  nécessaire pour publier sur le Play Store.

## 2. Préparer l'environnement local

```bash
cd mobile
npm install
npx eas-cli login          # connexion au compte Expo
npx eas-cli init           # cree le projet EAS et renseigne extra.eas.projectId dans app.json
```

Renseigner ensuite dans `app.json` :
- `owner` : ton compte ou organisation Expo (ex. `mg-assistance`).
- `extra.eas.projectId` : rempli automatiquement par `eas init`.

## 3. Build de test interne (recommandé avant la première soumission)

```bash
npx eas-cli build --platform android --profile preview   # genere un .apk installable directement
npx eas-cli build --platform ios --profile preview        # necessite un compte Apple Developer (ad hoc / internal)
```

Installer l'APK sur un téléphone Android de test, et distribuer le build
iOS via TestFlight (voir étape 5) avant de viser la publication publique.

## 4. Credentials de signature

### iOS
```bash
npx eas-cli credentials
```
EAS peut générer et gérer automatiquement le certificat de distribution et
le profil de provisioning (recommandé), à condition d'être connecté à un
compte Apple Developer actif. Renseigner ensuite dans `eas.json` →
`submit.production.ios` :
- `appleId` : l'email du compte Apple Developer.
- `ascAppId` : l'ID de l'app dans App Store Connect (créer l'app au
  préalable sur https://appstoreconnect.apple.com, bundle ID
  `sn.mgassistance.mgamobile`).
- `appleTeamId` : visible sur https://developer.apple.com/account →
  Membership.

### Android
1. Créer l'app sur Google Play Console (package `sn.mgassistance.mgamobile`).
2. Créer un compte de service dédié (Play Console → Utilisateurs et
   autorisations → API access) et télécharger sa clé JSON.
3. Enregistrer ce fichier en local sous
   `mobile/google-play-service-account.json` (déjà exclu du repo via
   `.gitignore` — **ne jamais le committer**).

## 5. Build de production + soumission

```bash
npx eas-cli build --platform all --profile production
npx eas-cli submit --platform ios --profile production
npx eas-cli submit --platform android --profile production
```

- **iOS** : la soumission place le build en revue TestFlight puis App
  Store (revue Apple : quelques heures à quelques jours). Remplir au
  préalable la fiche App Store Connect (captures d'écran, description,
  politique de confidentialité — obligatoire, l'app appelle une API
  distante).
- **Android** : `track: "internal"` dans `eas.json` publie d'abord sur la
  piste de test interne Play Console. Promouvoir manuellement vers
  `production` depuis la Play Console une fois validé.

## 6. Mises à jour ultérieures

- Nouvelle version avec changement natif (nouvelle dépendance native,
  changement de permission...) : incrémenter `version` dans `app.json`,
  relancer `eas build` + `eas submit`.
- Correctif JS/TS seul, sans changement natif : possibilité d'utiliser les
  **EAS Update** (OTA) sur les channels `preview`/`production` définis
  dans `eas.json`, sans repasser par la revue des stores :
  ```bash
  npx eas-cli update --channel production --message "Correctif ..."
  ```

## 7. Ce qui n'est pas encore fait (prochaines étapes)

- Générer les vrais visuels de marque (icône, splash) — voir section 0.
- Rédiger la politique de confidentialité (obligatoire pour la fiche App
  Store/Play Store, l'app traitant des données clients via l'API).
- Captures d'écran et fiche store (description FR, mots-clés).
- CI GitHub Actions pour déclencher `eas build` automatiquement sur tag de
  version (peut être ajoutée une fois le projet EAS initialisé et le
  secret `EXPO_TOKEN` disponible).
