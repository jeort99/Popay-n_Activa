FROM python:3.13-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar proyecto
COPY . .

# Puerto Django
EXPOSE 8000

# Comando inicial
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]