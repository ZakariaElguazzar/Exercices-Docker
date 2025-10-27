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

#Health Check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
 CMD curl -f http://localhost:3000/api/health || exit 1

# Commande de lancement
CMD ["npm", "start"]

