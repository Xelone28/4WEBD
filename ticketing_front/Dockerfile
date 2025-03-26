# Stage 1: Build React App
FROM node:18-alpine AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendance
COPY package.json ./
# COPY package-lock.json ./  # Si vous avez un fichier package-lock.json

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application
COPY . ./

# Construire l'application pour la production
RUN npm run build

# Stage 2: Serve React App avec Nginx
FROM nginx:1.21-alpine

# Copier les fichiers construits depuis le stage build
COPY --from=build /app/build /usr/share/nginx/html

# Copier la configuration nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Définir les permissions correctes pour le fichier de configuration
RUN chmod 644 /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Démarrer nginx
CMD ["nginx", "-g", "daemon off;"]