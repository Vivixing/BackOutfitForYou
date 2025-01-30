from beanie import Document, Link
from typing import List
from datetime import datetime
from models.UsuarioModel import Usuario
from models.VestuarioModel import Vestuario

class Recomendacion(Document):
    usuarioId: Link[Usuario]
    ocasion: str
    vestuarioSugerido: List[Link[Vestuario]]=[]
    fechaCreado: datetime

    class Settings:
        collection = "recomendaciones"