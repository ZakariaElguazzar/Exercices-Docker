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

