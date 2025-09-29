from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from .UsuarioModel import Usuario
from .VestuarioModel import Vestuario

class VisualizacionModel(BaseModel):
    usuarioId: PydanticObjectId
    vestuarioId: PydanticObjectId
    imagen: str
    fechaCreado: datetime

class Visualizacion(VisualizacionModel, Document):
    usuarioId: Link[Usuario]
    vestuarioId: Link[Vestuario]

    class Settings:
        collection = "visualizaciones"
        indexes = [
            ("usuarioId.$id")
        ]