````markdown
# Exercice Docker – Manipulation avancée des conteneurs

---

## Objectifs pédagogiques
- Comprendre le fonctionnement des conteneurs en mode interactif.  
- Apprendre à installer des outils dans un conteneur.  
- Manipuler des fichiers entre le système hôte et un conteneur.  
- Créer une image Docker personnalisée à partir d’un conteneur existant.

---

## Étapes de l’exercice

### 1. Lancer un conteneur Ubuntu en mode interactif
```bash
docker run -it --name ubuntu-test ubuntu:latest
````

Cette commande télécharge (si nécessaire) l’image Ubuntu et ouvre une session interactive dans le conteneur.

* `-it` : permet d’interagir avec le conteneur via le terminal.
* `--name` : attribue un nom pour faciliter les manipulations ultérieures.

---

### 2. Installer les outils `curl` et `vim` dans le conteneur

```bash
apt update
apt install -y curl vim
```

* `apt update` met à jour la liste des paquets disponibles.
* `apt install` installe les outils nécessaires à la manipulation et l’édition de fichiers.

---

### 3. Créer un fichier `test.txt` avec du contenu

```bash
echo "Bonjour depuis le conteneur Ubuntu !" > test.txt
cat test.txt
```

Cette commande crée un fichier texte contenant une phrase simple.
L’affichage via `cat` permet de vérifier la création du fichier.

---

### 4. Sortir du conteneur sans l’arrêter

Utiliser le raccourci clavier :

```
Ctrl + P puis Ctrl + Q
```

Cette combinaison quitte la session interactive tout en laissant le conteneur actif.
Pour vérifier son état :

```bash
docker ps
```

---

### 5. Copier le fichier `test.txt` du conteneur vers la machine hôte

```bash
docker cp ubuntu-test:/test.txt ./test.txt
```

Le fichier présent dans le conteneur est copié dans le répertoire courant de la machine hôte.

---

### 6. Modifier le fichier sur la machine hôte et le recopier dans le conteneur

#### a. Modification du fichier :

```bash
echo "Fichier modifié depuis l’hôte." >> test.txt
cat test.txt
```

#### b. Recopie dans le conteneur :

```bash
docker cp test.txt ubuntu-test:/test.txt
```

Cette commande remplace le fichier dans le conteneur par la version modifiée.

---

### 7. Reconnexion au conteneur et vérification des modifications

```bash
docker exec -it ubuntu-test bash
cat /test.txt
```

La commande `docker exec` permet de rouvrir une session dans le conteneur déjà en cours d’exécution.
Le contenu du fichier doit refléter les modifications effectuées sur la machine hôte.

---

### 8. Créer une nouvelle image à partir du conteneur modifié

```bash
docker commit ubuntu-test ubuntu-custom:1.0
```

Cette commande crée une image Docker appelée `ubuntu-custom` (version 1.0) basée sur l’état actuel du conteneur `ubuntu-test`.

---

### 9. Lancer un nouveau conteneur basé sur l’image personnalisée

```bash
docker run -it --name ubuntu-new ubuntu-custom:1.0
```

Le conteneur ainsi créé hérite de toutes les modifications effectuées dans l’image personnalisée.

---

### 10. Vérifier la présence des modifications dans le nouveau conteneur

```bash
cat /test.txt
```

Le fichier `test.txt` doit contenir le texte modifié précédemment, confirmant la bonne persistance des changements dans l’image.

---
