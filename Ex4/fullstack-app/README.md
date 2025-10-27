````markdown
# Exercice Docker Compose – Orchestration d’une application fullstack

**Durée estimée :** 60 minutes  
**Contexte :** Containerisation et orchestration d’une application web avec base de données PostgreSQL et cache Redis à l’aide de Docker Compose.

---

## Objectifs pédagogiques
- Développer une application Python Flask avec persistance des données et cache.  
- Créer et configurer une stack multi-conteneurs avec Docker Compose.  
- Mettre en place des volumes persistants, variables d’environnement et dépendances entre services.  
- Ajouter des outils d’administration et des health checks pour monitorer les services.  

---

## Architecture de la stack
| Service | Image / Technologie | Rôle |
|---------|-------------------|------|
| web     | Python Flask      | Application principale exposant l’API CRUD pour les utilisateurs |
| db      | PostgreSQL        | Base de données relationnelle pour stocker les utilisateurs |
| cache   | Redis             | Cache pour gérer les sessions ou accélérer certaines requêtes |
| adminer | Adminer           | Interface web pour administrer PostgreSQL |

---

## Étapes de l’exercice

### 1. Créer le dossier du projet
```bash
mkdir fullstack-app
cd fullstack-app
````

---

### 2. Développer l’API Flask

Exemple minimal de structure de fichiers :

```
fullstack-app/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── requirements.txt
└── docker-compose.yml
```

#### a. `requirements.txt`

```text
Flask==2.3.2
psycopg2-binary==2.9.7
redis==5.3.0
Flask_SQLAlchemy==3.0.5
```

#### b. Exemple minimal `app/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os

db = SQLAlchemy()
cache = Redis(host='cache', port=6379)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/usersdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
```

#### c. Exemple minimal `app/routes.py`

```python
from flask import Blueprint, request, jsonify
from . import db
from .models import User

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Ajoutez ici d’autres routes CRUD pour create, update, delete
```

---

### 3. Créer le `docker-compose.yml`

```yaml
version: '3.9'

services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    depends_on:
      - db
      - cache
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/usersdb
      - REDIS_HOST=cache
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: usersdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 5s
      retries: 5

  cache:
    image: redis:8-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 5

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  pgdata:
```

---

### 4. Configurer les volumes persistants

* Le volume `pgdata` est monté sur `/var/lib/postgresql/data` pour garantir la **persistance des données** PostgreSQL même si le conteneur est supprimé.

---

### 5. Ajouter les variables d’environnement

* Définir `DATABASE_URL` pour Flask et `REDIS_HOST` pour Redis.
* Définir `POSTGRES_USER`, `POSTGRES_PASSWORD` et `POSTGRES_DB` pour PostgreSQL.

---

### 6. Configurer les dépendances entre services

* `depends_on` assure que `web` attend que `db` et `cache` soient démarrés.
* Health checks permettent d’assurer que les services sont **opérationnels avant de dépendre dessus**.

---

### 7. Lancer la stack complète

```bash
docker-compose up -d
```

---

### 8. Tester la connectivité entre les services

* Vérifier que Flask peut accéder à PostgreSQL et Redis.
* Exemple de test :

```bash
docker-compose exec web python
>>> from app import db, cache
>>> db.session.execute('SELECT 1')
>>> cache.ping()
```

---

### 9. Ajouter un service Adminer

* Adminer permet d’administrer PostgreSQL via l’interface web accessible sur `http://localhost:8080`.

---

### 10. Implémenter des health checks pour tous les services

* Déjà inclus dans le `docker-compose.yml` pour `web`, `db` et `cache`.
* Vérifier avec :

```bash
docker-compose ps
docker inspect <container_name> | grep Health
```

---

