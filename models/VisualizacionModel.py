from typing import List
from beanie import Document, Link
from datetime import datetime
from models.UsuarioModel import Usuario
from models.VestuarioModel import Vestuario

class Visualizacion(Document):
    usuarioId: Link[Usuario]
    vestuarioId: List[Link[Vestuario]]=[]
    imagen: str
    fechaCreado: datetime

    class Settings:
        collection = "visualizaciones"