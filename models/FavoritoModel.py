from beanie import Document, Link
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class FavoritoModel(BaseModel):
    usuarioId: str 
    vestuarioId: str
    fechaCreado: datetime
    estado: bool

    class Settings:
        collection = "favoritos"

class Favorito(FavoritoModel, Document):
    usuarioId: Link[Usuario]  
    vestuarioId: Link[Vestuario]
