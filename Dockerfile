# Imagen base
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential

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
CMD ["uvicorn", "main:app", "--host",  "0.0.0.0", "--port", "8000"]
