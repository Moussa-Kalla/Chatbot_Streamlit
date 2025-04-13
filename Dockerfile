FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système, y compris supervisor et curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer le client Ollama (exemple, adapter si besoin)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copier le projet
COPY . .

# Rendre exécutable le script principal de Streamlit
RUN chmod +x app/main.py

EXPOSE 8501

# Copie de la configuration Supervisor
# Créer le fichier /etc/supervisor/conf.d/supervisord.conf avec le contenu suivant:
#
# [supervisord]
# nodaemon=true
#
# [program:streamlit]
# command=streamlit run /app/main.py --server.port=8501 --server.address=0.0.0.0
# directory=/app
# autostart=true
# autorestart=true
# stdout_logfile=/dev/stdout
# stderr_logfile=/dev/stderr
#
# [program:ollama]
# command=/bin/sh -c "ollama run llama3.2:1b && ollama run gemma3:1b && ollama run deepseek-r1:1.5b && ollama run qwen2.5:0.5b && tail -f /dev/null"
# autostart=true
# autorestart=false
# stdout_logfile=/dev/stdout
# stderr_logfile=/dev/stderr
#
COPY .devcontainer/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Lancer Supervisor en point d'entrée pour démarrer les deux services
CMD ["/usr/bin/supervisord"]