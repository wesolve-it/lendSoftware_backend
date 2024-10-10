# Dockerfile für Django
FROM python:3.9

# Installiere Abhängigkeiten
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Kopiere requirements.txt
COPY requirements.txt .

# Upgrade pip und installiere Abhängigkeiten
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest deines Anwendungscodes
COPY . .

#EXPOSE 8000

# Führe deine App aus
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]