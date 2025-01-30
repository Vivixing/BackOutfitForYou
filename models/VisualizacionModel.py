from typing import List
from beanie import Document, Link
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import UsuarioModel
from .VestuarioModel import VestuarioModel

class VisualizacionModel(BaseModel):
    usuarioId: str
    vestuarioId: List[str]=[]
    imagen: str
    fechaCreado: datetime

    class Settings:
        collection = "visualizaciones"

class Visualizacion(VisualizacionModel, Document):
    usuarioId: Link[UsuarioModel]
    vestuarioId: List[Link[VestuarioModel]]=[]
