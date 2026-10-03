# Wallet App : API de portefeuille électronique

API REST (backend uniquement) pour une application de portefeuille électronique, développée avec **Django** et **Django REST Framework**. Un utilisateur peut créer un compte, s'authentifier avec JWT, disposer d'un portefeuille, déposer, retirer et transférer de l'argent, puis consulter l'historique de ses transactions.

## Fonctionnalités

- Inscription et connexion par numéro de téléphone (JWT : access token et refresh token)
- Consultation et modification du profil
- Portefeuille créé automatiquement à l'inscription (solde initial : 0)
- Dépôt et retrait avec validation du montant et vérification du solde
- Transfert entre utilisateurs par numéro de téléphone (atomique)
- Historique des transactions avec filtres (type, date) et pagination
- Chaque utilisateur n'accède qu'à ses propres données
- Administration Django pour consulter utilisateurs, wallets et transactions

## Technologies

- Python 3
- Django
- Django REST Framework
- djangorestframework-simplejwt (authentification JWT)
- SQLite (base de données par défaut)
- Postman (tests des endpoints)

## Structure du projet

```
wallet_project/
├── manage.py
├── requirements.txt
├── wallet_project/        # Configuration (settings.py, urls.py)
├── users/                 # Modèle utilisateur, inscription, connexion, profil
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── wallet/                # Portefeuille : solde, dépôt, retrait, transfert
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── transactions/          # Historique des transactions
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## Installation

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd wallet_project

# 2. Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

Si le fichier `requirements.txt` est absent, installer directement :

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

## Lancement

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser    # facultatif : accès à /admin/
python manage.py runserver
```

L'API est disponible sur : `http://127.0.0.1:8000/api/`

Pour créer un superutilisateur, le numéro de téléphone sert d'identifiant. Django demande aussi le nom, le prénom et le NNI.

## Authentification

Les endpoints protégés demandent un token JWT dans l'en-tête :

```
Authorization: Bearer <access_token>
```

- Le token d'accès est valable **30 minutes**.
- Le refresh token est valable **7 jours** et permet d'obtenir un nouveau token d'accès.

## Endpoints

| Méthode | Endpoint | Description | Authentification |
|---|---|---|---|
| POST | `/api/auth/register/` | Inscription | Non |
| POST | `/api/auth/login/` | Connexion (access + refresh token) | Non |
| POST | `/api/auth/login/refresh/` | Renouveler le token d'accès | Non |
| GET | `/api/profile/` | Voir le profil | Oui |
| PUT | `/api/profile/` | Modifier le profil | Oui |
| GET | `/api/wallet/` | Voir le solde | Oui |
| POST | `/api/wallet/deposit/` | Déposer de l'argent | Oui |
| POST | `/api/wallet/withdraw/` | Retirer de l'argent | Oui |
| POST | `/api/wallet/transfer/` | Transférer de l'argent | Oui |
| GET | `/api/transactions/` | Historique des transactions | Oui |

## Exemples de requêtes

### Inscription

`POST /api/auth/register/`

```json
{
  "name": "Mohamed",
  "prenom": "Ahmed",
  "NNI": "1234567890",
  "nb_telephone": "22212345678",
  "password": "MotDePasse@2026"
}
```

Réponse `201 Created` :

```json
{
  "message": "Utilisateur créé avec succès.",
  "user_id": 1
}
```

Le mot de passe doit respecter les validateurs de Django (longueur minimale, pas trop courant, pas entièrement numérique, pas trop proche des autres informations). Le `NNI` et le numéro de téléphone doivent être uniques.

### Connexion

`POST /api/auth/login/`

```json
{
  "nb_telephone": "22212345678",
  "password": "MotDePasse@2026"
}
```

Réponse `200 OK` :

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Renouveler le token

`POST /api/auth/login/refresh/`

```json
{
  "refresh": "<refresh_token>"
}
```

### Profil

`GET /api/profile/` retourne :

```json
{
  "user_id": 1,
  "name": "Mohamed",
  "prenom": "Ahmed",
  "NNI": "1234567890",
  "nb_telephone": "22212345678",
  "type_user": "client",
  "solde": "0.00"
}
```

`PUT /api/profile/` modifie le nom et le prénom (envoi partiel accepté) :

```json
{
  "name": "Mohamed",
  "prenom": "Ali"
}
```

Les champs `user_id`, `NNI`, `nb_telephone` et `type_user` sont en lecture seule.

### Consulter le solde

`GET /api/wallet/`

```json
{
  "wallet_id": 1,
  "solde": "500.00"
}
```

### Dépôt

`POST /api/wallet/deposit/`

```json
{
  "montant": 500
}
```

Réponse `200 OK` :

```json
{
  "message": "Dépôt effectué avec succès.",
  "solde": "500.00"
}
```

### Retrait

`POST /api/wallet/withdraw/`

```json
{
  "montant": 100
}
```

Réponse `200 OK` :

```json
{
  "message": "Retrait effectué avec succès.",
  "solde": "400.00"
}
```

### Transfert

`POST /api/wallet/transfer/`

```json
{
  "montant": 50,
  "nb_telephone_destinataire": "22287654321"
}
```

Réponse `200 OK` :

```json
{
  "message": "Transfert effectué avec succès.",
  "solde": "350.00"
}
```

### Historique des transactions

`GET /api/transactions/`

Réponse paginée (10 résultats par page) :

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "trans_id": 3,
      "montant": "50.00",
      "date_trans": "2026-10-03T10:15:00Z",
      "type_trans": "envoi",
      "statut_trans": "effectué",
      "telephone_expediteur": "22212345678",
      "telephone_destinataire": "22287654321"
    }
  ]
}
```

Le champ `type_trans` est adapté à l'utilisateur connecté : `depot`, `retrait`, `envoi` (transfert envoyé) ou `recoit` (transfert reçu).

**Filtres disponibles :**

| Paramètre | Exemple | Effet |
|---|---|---|
| `type` | `?type=depot` | Filtre par type : `depot`, `retrait` ou `transfert` |
| `date` | `?date=2026-10-03` | Transactions d'une date exacte |
| `date_from` | `?date_from=2026-10-01` | À partir d'une date |
| `date_to` | `?date_to=2026-10-31` | Jusqu'à une date |
| `page` | `?page=2` | Page des résultats |

Les filtres peuvent être combinés : `/api/transactions/?type=transfert&date_from=2026-10-01&page=1`

## Codes de réponse et erreurs

| Code | Cas |
|---|---|
| 200 | Opération réussie |
| 201 | Utilisateur créé |
| 400 | Montant invalide (négatif ou nul), solde insuffisant, auto-transfert, données invalides |
| 401 | Token absent, invalide ou expiré |
| 404 | Destinataire introuvable |

Exemples de messages d'erreur :

```json
{ "error": "Solde insuffisant pour effectuer le retrait." }
{ "error": "Solde insuffisant." }
{ "error": "Le destinataire n'existe pas." }
{ "error": "Vous ne pouvez pas transférer de l'argent à vous-même." }
```

Les erreurs de validation (montant négatif, champ manquant, etc.) sont renvoyées par champ :

```json
{ "montant": ["Ensure this value is greater than or equal to 0.01."] }
```

## Modèle de données

Trois entités :

- **user** : `user_id` (clé primaire), `name`, `prenom`, `NNI` (unique), `nb_telephone` (unique, identifiant de connexion), `type_user` (`client`, `agence` ou `admin`), `is_active`, `is_staff`.
- **wallet** : `wallet_id` (clé primaire), `solde` (décimal, 0 par défaut), `user` (relation OneToOne avec user).
- **transaction** : `trans_id` (clé primaire), `montant`, `date_trans` (automatique), `type_trans` (`transfert`, `depot`, `retrait`), `statut_trans` (`en attente`, `effectué`, `annulé`), `wallet_expediteur`, `wallet_destinataire`, `deposent` (trois ForeignKey vers wallet).

**Relations :**

- user ↔ wallet : **OneToOne** (un utilisateur, un wallet).
- wallet → transaction : **trois ForeignKey** (un wallet peut avoir plusieurs transactions).

**Choix de conception :** un seul modèle `transaction` générique. Un transfert est enregistré en **une seule ligne** liée aux deux wallets (`wallet_expediteur` et `wallet_destinataire`). Un dépôt ou un retrait utilise le champ `deposent`. Le sens (envoi ou reçu) est calculé à l'affichage selon l'utilisateur connecté. `on_delete=SET_NULL` conserve l'historique si un wallet est supprimé.

## Sécurité et cohérence

- Authentification JWT sur tous les endpoints, sauf inscription et connexion.
- Chaque requête utilise l'utilisateur connecté (`request.user`) : chacun ne voit que ses propres données.
- Le `type_user` est forcé à `client` à l'inscription.
- Montants validés avec `min_value=0.01` (pas de valeur négative ou nulle).
- Soldes stockés en `DecimalField` (pas de float, donc pas d'erreur d'arrondi).
- Dépôt, retrait et transfert sont exécutés dans `transaction.atomic()` : si une étape échoue, rien n'est enregistré.
- `select_for_update()` verrouille les wallets pendant l'opération pour éviter les accès simultanés.

## Tests avec Postman

1. Importer le fichier de collection `.json` fourni dans Postman.
2. Créer un environnement avec les variables :
   - `base_url` = `http://127.0.0.1:8000`
   - `access_token` = token obtenu après la connexion
3. Les requêtes protégées utilisent l'en-tête `Authorization: Bearer {{access_token}}`.

La collection est organisée en dossiers :

- **Auth** : inscription, connexion, refresh, profil
- **Wallet** : solde, dépôt, retrait, transfert
- **Transactions** : historique, filtres, pagination

Chaque endpoint est testé avec des cas valides et des cas d'erreur (montant négatif, solde insuffisant, destinataire inconnu, auto-transfert, requête sans token).

## Administration

L'interface d'administration est disponible sur `http://127.0.0.1:8000/admin/` avec un compte superutilisateur. Elle permet de consulter les utilisateurs, les wallets et les transactions, avec recherche et filtres.

## Axes d'amélioration

- Code PIN à 4 chiffres pour valider un transfert ou un retrait
- Limite de transfert journalière
- Notifications simulées après chaque transaction
- Tests automatisés (tests unitaires Django)
- Pour la production : `SECRET_KEY` dans une variable d'environnement, `DEBUG = False`, PostgreSQL, documentation Swagger

## Auteur

Projet réalisé dans le cadre du mini-projet de fin de formation Django et Postman.
