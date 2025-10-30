# 1️⃣ Basis-Image
FROM python:3.9

# 2️⃣ Arbeitsverzeichnis
WORKDIR /app

# 3️⃣ Systemabhängigkeiten installieren
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# 4️⃣ Python-Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Projekt kopieren
COPY . .

# 6️⃣ Port, auf dem Django läuft
EXPOSE 8000

# 7️⃣ Standardbefehl: Gunicorn für Produktion
#    Für Entwicklung kannst du "python manage.py runserver 0.0.0.0:8000" benutzen
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
