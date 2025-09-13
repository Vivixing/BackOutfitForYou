from typing import List
from beanie import Document, Link
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class VisualizacionModel(BaseModel):
    usuarioId: str
    vestuarioId: str
    imagen: str
    fechaCreado: datetime

    class Settings:
        collection = "visualizaciones"

class Visualizacion(VisualizacionModel, Document):
    usuarioId: Link[Usuario]
    vestuarioId: Link[Vestuario]
