# Utilisation de l'image officielle Python 3.9 Slim
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copie uniquement le fichier requirements.txt pour optimiser le cache Docker
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code de l'application
COPY . .

# Rendre le fichier main.py exécutable
RUN chmod +x app/main.py

# Exposition du port utilisé par Streamlit
EXPOSE 8501

# Ajout d'un HEALTHCHECK pour surveiller l'état de l'application
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD streamlit health-check || exit 1

# Lancement de l'application avec Streamlit
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]