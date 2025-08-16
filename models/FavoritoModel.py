from beanie import Document, Link
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class FavoritoModel(BaseModel):
    usuarioId: str 
    vestuarioId: List[str] = []
    fechaCreado: datetime

    class Settings:
        collection = "favoritos"

class Favorito(FavoritoModel, Document):
    usuarioId: Link[Usuario]  
    vestuarioId: List[Link[Vestuario]] = []
