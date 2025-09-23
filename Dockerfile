# Imagen base
FROM python:3.11.4-slim

# Crear directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia el código de tu aplicación FastAPI al directorio de trabajo
COPY . .

# Exponer el puerto que Render asigna dinámicamente
EXPOSE 10000

# Comando de arranque (Render pasará su $PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]
