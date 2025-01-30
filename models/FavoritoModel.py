from beanie import Document, Link
from datetime import datetime
from typing import List
from models.UsuarioModel import Usuario
from models.VestuarioModel import Vestuario

class Favorito(Document):
    usuarioId: Link[Usuario]
    vestuarioId: List[Link[Vestuario]]=[]
    fechaCreado: datetime

    class Settings:
        collection = "favoritos"