from beanie import Document, Link
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .UsuarioModel import UsuarioModel
from .VestuarioModel import VestuarioModel

class RecomendacionModel(BaseModel):
    usuarioId: str
    ocasion: str
    vestuarioSugerido: List[str] = []
    fechaCreado: datetime

    class Settings:
        collection = "recomendaciones"

class Recomendacion(RecomendacionModel,Document):
    usuarioId: Link[UsuarioModel]
    vestuarioSugerido: List[Link[VestuarioModel]]=[]
