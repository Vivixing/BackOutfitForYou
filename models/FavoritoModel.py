from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class FavoritoModel(BaseModel):
    usuarioId: PydanticObjectId
    vestuarioId: PydanticObjectId
    fechaCreado: datetime
    estado: bool

class Favorito(FavoritoModel, Document):
    usuarioId: Link[Usuario]  
    vestuarioId: Link[Vestuario]

    class Settings:
        collection = "favoritos"
        indexes = [
            [("usuarioId.$id", 1), ("estado", 1)]
        ]