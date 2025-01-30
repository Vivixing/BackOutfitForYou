from beanie import Document, Link
from typing import List
from datetime import datetime
from models.UsuarioModel import Usuario
from models.PrendaModel import Prenda

class Vestuario(Document):
    usuarioId: Link[Usuario]
    prendas: List[Link[Prenda]]=[]
    ocasion: str
    fechaCreacion: datetime

    class Settings:
        collection = "vestuarios"