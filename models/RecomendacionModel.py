from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class RecomendacionModel(BaseModel):
    usuarioId: PydanticObjectId
    ocasion: str
    vestuarioSugerido: str 
    fechaCreado: datetime

    class Settings:
        collection = "recomendaciones"

class Recomendacion(RecomendacionModel,Document):
    usuarioId: Link[Usuario]
    vestuarioSugerido: Link[Vestuario]
