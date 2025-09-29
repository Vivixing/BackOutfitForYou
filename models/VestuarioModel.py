from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .PrendaModel import Prenda
from .UsuarioModel import Usuario

class VestuarioModel(BaseModel):
    usuarioId: PydanticObjectId
    prendas: List[str] = []
    fechaCreacion: datetime

class Vestuario(VestuarioModel, Document):
    usuarioId: Link[Usuario]
    prendas: List[Link[Prenda]]=[]

    class Settings:
        collection = "vestuarios"
        indexes = [
            ("usuarioId.$id")
        ]

