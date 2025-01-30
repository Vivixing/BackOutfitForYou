from beanie import Document, Link
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .PrendaModel import PrendaModel
from .UsuarioModel import UsuarioModel

class VestuarioModel(BaseModel):
    usuarioId: str
    prendas: List[str] = []
    ocasion: str
    fechaCreacion: datetime

    class Settings:
        collection = "vestuarios"

class Vestuario(VestuarioModel, Document):
    usuarioId: Link[UsuarioModel]
    prendas: List[Link[PrendaModel]]=[]

    