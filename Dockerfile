FROM python:3.13-slim

WORKDIR /app

# Installer les dépendances système, y compris supervisor et curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip
RUN pip install --upgrade pip

# Copier les fichiers nécessaires pour l'installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer le client Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Ensure the Ollama directory exists and has the correct permissions
RUN mkdir -p /root/.ollama && chmod -R 755 /root/.ollama

# Copier tout le projet dans le conteneur
COPY . .

# Assurer les permissions correctes pour tous les fichiers
RUN chmod -R 755 /app

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Copier la configuration Supervisor
COPY .devcontainer/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Lancer Supervisor en point d'entrée pour démarrer les deux services
CMD ["/usr/bin/supervisord"]

RUN ls -l /app/app