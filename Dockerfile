# Usamos imagen oficial de Python 3.12 slim
FROM python:3.12-slim

# Instalamos dependencias del sistema, incluido postgresql-client para pg_isready
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Seteamos directorio de trabajo
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la app
COPY . .

# Expone el puerto donde correrá Django
EXPOSE 8000

# El comando se sobrescribirá en docker-compose.yml
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
