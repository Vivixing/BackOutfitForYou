from beanie import Document, Link, PydanticObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .TipoPrendaModel import TipoPrendaModel
from .UsuarioModel import UsuarioModel

class PrendaModel(BaseModel):
    usuarioId: PydanticObjectId
    tipoPrendaId: PydanticObjectId
    nombre: str
    color: str
    imagen: str 
    fechaCreado: datetime = Field(default_factory=datetime.now)
    fechaModificado: datetime = Field(default_factory=datetime.now)
    estado: bool = Field(default=True)

class Prenda(Document, PrendaModel):
    usuarioId: Link[UsuarioModel] 
    tipoPrendaId: Link[TipoPrendaModel]

    class Settings:
        collection = "prendas"


    