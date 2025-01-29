from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

#Cargar las variables de entorno
load_dotenv()

# Obtener la URI de la base de datos de las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")

# Crear una instancia de MongoClient
client = MongoClient(MONGO_URI)

# Confirmar conexión a la base de datos
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)





