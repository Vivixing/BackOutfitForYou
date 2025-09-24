# Imagen base
FROM python:3.11.4-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación FastAPI al directorio de trabajo
COPY . .

# Exponer el puerto que Render asigna dinámicamente
EXPOSE 8000

# Comando de arranque (Render pasará su $PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
