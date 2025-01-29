from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "oufitForYou"

#Cliente Mongo
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

#Colecciones
usuario_collection = database.get_collection("usuario")
prenda_collection = database.get_collection("prenda")
tipoPrenda_collection = database.get_collection("tipoPrenda")
vestuario_collection = database.get_collection("vestuario")
favorito_collection = database.get_collection("favorito")
recomendacion_collection = database.get_collection("recomendacion")
visualizacion_collection = database.get_collection("visualizacion")