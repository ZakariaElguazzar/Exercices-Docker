````markdown
# Exercice Docker – Containerisation d’une application web Node.js

## Étapes de l’exercice

### 1. Créer le dossier du projet
```bash
mkdir node-app
cd node-app
````

---

### 2. Créer les fichiers nécessaires

#### a. `package.json`

Configuration de base pour Node.js et Express :

```json
{
  "name": "node-app",
  "version": "1.0.0",
  "description": "Application web containerisée avec Docker",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

#### b. `server.js`

Serveur Express avec plusieurs routes :

```javascript
const express = require('express');
const app = express();
const port = 3000;

// Route d'accueil
app.get('/', (req, res) => {
    res.send('Bienvenue sur la page d’accueil !');
});

// Route health
app.get('/api/health', (req, res) => {
    res.json({ status: 'UP' });
});

// Route info
app.get('/api/info', (req, res) => {
    res.json({
        nodeVersion: process.version,
        platform: process.platform,
        memory: process.memoryUsage()
    });
});

// Route time
app.get('/api/time', (req, res) => {
    res.json({ time: new Date().toISOString() });
});

app.listen(port, () => {
    console.log(`Serveur lancé sur http://localhost:${port}`);
});
```

#### c. `.dockerignore`

Pour réduire la taille de l’image et exclure les fichiers inutiles :

```
node_modules
npm-debug.log
```

#### d. `Dockerfile` initial

```dockerfile
# Utiliser une image officielle Node.js
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install --production

# Copier le reste des fichiers
COPY . .

# Exposer le port
EXPOSE 3000

# Commande de lancement
CMD ["npm", "start"]
```

---

### 3. Construire l’image Docker

```bash
docker build -t node-app:1.0 .
```

---

### 4. Lancer le conteneur sur le port 3000

```bash
docker run -d -p 3000:3000 --name node-app node-app:1.0
```

---

### 5. Tester toutes les routes

* `GET /` → Accueil
* `GET /api/health` → Status de l’application
* `GET /api/info` → Informations environnement
* `GET /api/time` → Heure actuelle

Par exemple avec `curl` :

```bash
curl http://localhost:3000/
curl http://localhost:3000/api/health
curl http://localhost:3000/api/info
curl http://localhost:3000/api/time
```

---

### 6. Optimiser le Dockerfile pour réduire la taille de l’image

* Utiliser l’image `node:18-alpine` (déjà légère).
* Copier seulement les fichiers nécessaires (`package*.json`) avant d’installer les dépendances.
* Ajouter `.dockerignore` pour exclure les fichiers inutiles.

---

### 7. Reconstruire l’image optimisée

```bash
docker build -t node-app:1.1 .
```

---

### 8. Comparer les tailles des images

```bash
docker images node-app
```

> Comparer la taille de `node-app:1.0` et `node-app:1.1` pour observer l’impact de l’optimisation.

---

### 9. Ajouter un health check dans le Dockerfile

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
 CMD curl -f http://localhost:3000/api/health || exit 1
```

---

### 10. Tester le health check

```bash
docker inspect --format='{{json .State.Health}}' node-app
```

> Cette commande permet de vérifier l’état de santé du conteneur.

---
