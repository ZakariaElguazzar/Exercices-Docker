````markdown
# Exercice Docker – Introduction aux Conteneurs

## Objectif
L’objectif de cet exercice est de se familiariser avec les commandes de base de Docker.  
Il s’agit d’apprendre à manipuler des images et des conteneurs, à exécuter des services simples et à comprendre les principes fondamentaux de l’isolation et de la gestion des ressources.

---

## Étapes de l’exercice

### 1. Vérifier que Docker Desktop est bien installé et démarré
```bash
docker --version
docker info
````

Ces commandes permettent de s’assurer que Docker est correctement installé et en cours d’exécution sur la machine.

---

### 2. Exécuter un premier conteneur avec l’image *hello-world*

```bash
docker run hello-world
```

Cette commande télécharge et exécute une image de test qui confirme le bon fonctionnement de l’installation Docker.

---

### 3. Télécharger l’image *nginx:alpine* sans la lancer

```bash
docker pull nginx:alpine
```

L’option `pull` permet de récupérer une image depuis Docker Hub sans démarrer de conteneur.

---

### 4. Lister les images présentes sur le système

```bash
docker images
```

Affiche la liste des images locales avec leur identifiant, leur taille et leur origine.

---

### 5. Lancer un conteneur Nginx en arrière-plan sur le port 8080

```bash
docker run -d -p 8080:80 --name mon-nginx nginx:alpine
```

* `-d` : exécution en mode détaché (arrière-plan).
* `-p 8080:80` : redirection du port 8080 de l’hôte vers le port 80 du conteneur.
* `--name` : attribue un nom au conteneur pour simplifier sa gestion.

---

### 6. Vérifier l’accessibilité du serveur web

Accéder à l’adresse suivante dans un navigateur :

```
http://localhost:8080
```

La page d’accueil par défaut de Nginx doit s’afficher.

---

### 7. Afficher les journaux du conteneur Nginx

```bash
docker logs mon-nginx
```

Cette commande permet de visualiser les messages générés par le processus Nginx dans le conteneur.

---

### 8. Lister tous les conteneurs (actifs et inactifs)

```bash
docker ps        # conteneurs actifs
docker ps -a     # tous les conteneurs, y compris ceux arrêtés
```

---

### 9. Arrêter et supprimer le conteneur Nginx

```bash
docker stop mon-nginx
docker rm mon-nginx
```

Ces commandes arrêtent puis suppriment le conteneur du système.

---

### 10. Nettoyer les images inutilisées

```bash
docker image prune -a
```

Supprime toutes les images non associées à un conteneur actif, afin de libérer de l’espace disque.

---

## Questions de réflexion

### 1. Différence entre une image et un conteneur

Une **image** Docker est un modèle immuable contenant les fichiers nécessaires à l’exécution d’une application (code, dépendances, configuration, etc.).
Un **conteneur** est une instance en cours d’exécution d’une image.

* L’image est statique (comme une recette).
* Le conteneur est dynamique (comme le plat cuisiné à partir de cette recette).

Ainsi, plusieurs conteneurs peuvent être créés à partir d’une même image.

---

### 2. Rôle de l’option `-d` lors du lancement d’un conteneur

L’option `-d` (pour *detached mode*) permet de lancer un conteneur en arrière-plan.

* Sans cette option, le terminal reste bloqué par la sortie standard du conteneur.
* Avec `-d`, le conteneur fonctionne de manière autonome, et l’utilisateur peut continuer à exécuter d’autres commandes.

Cette option est particulièrement utile pour les services ou serveurs (comme Nginx) qui doivent rester actifs sans bloquer le terminal.


