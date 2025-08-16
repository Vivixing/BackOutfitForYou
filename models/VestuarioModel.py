from beanie import Document, Link
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .PrendaModel import Prenda
from .UsuarioModel import Usuario

class VestuarioModel(BaseModel):
    usuarioId: str
    prendas: List[str] = []
    fechaCreacion: datetime

    class Settings:
        collection = "vestuarios"

class Vestuario(VestuarioModel, Document):
    usuarioId: Link[Usuario]
    prendas: List[Link[Prenda]]=[]

