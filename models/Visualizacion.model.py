from pydantic import BaseModel, ObjectId
from datetime import datetime

class Visualizacion(BaseModel):
    _id: ObjectId
    usuarioId: ObjectId
    vestuarioId: ObjectId
    imagen: str
    fechaCreado: datetime