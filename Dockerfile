# Gebruik een kleine Python-image
FROM python:3.10-slim

# Zet werkdirectory
WORKDIR /app

# Kopieer projectbestanden
COPY . .

# Installeer dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Zet environment variables voor Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expose poort
EXPOSE 5000

# Start de app
CMD ["flask", "run"]
