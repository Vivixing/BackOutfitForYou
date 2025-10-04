from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import os
from models.FavoritoModel import Favorito
from models.PrendaModel import Prenda
from models.RecomendacionModel import Recomendacion
from models.TipoPrendaModel import TipoPrenda
from models.UsuarioModel import Usuario
from models.VestuarioModel import Vestuario
from models.VisualizacionModel import Visualizacion 

async def init_db():
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")

    client = AsyncIOMotorClient(MONGO_URI)

    db = client["oufitForYou"]

    # Confirmar conexión a la base de datos
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        # Crear las colecciones
        await init_beanie(
            database=db,
            document_models=[Usuario, Prenda, TipoPrenda, Vestuario, Recomendacion, Visualizacion, Favorito ]
        )
        print("Colecciones creadas")
    except Exception as e:
        print(e)

    
    





