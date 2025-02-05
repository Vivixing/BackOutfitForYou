from beanie import Document, Link, PydanticObjectId
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .TipoPrendaModel import TipoPrendaModel
from .UsuarioModel import UsuarioModel

class PrendaModel(BaseModel):
    usuarioId: PydanticObjectId
    tipoPrendaId: PydanticObjectId
    nombre: str
    color: Optional[str]
    imagen: str
    fechaCreado: datetime
    fechaModificado: datetime

    class Settings:
        collection = "prendas"

class Prenda(PrendaModel, Document):
    usuarioId: Link[UsuarioModel]
    tipoPrendaId: Link[TipoPrendaModel]
    