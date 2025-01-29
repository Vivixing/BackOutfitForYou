from pydantic import BaseModel, ObjectId
from typing import Optional
from datetime import datetime

class Vestuario(BaseModel):
    _id: ObjectId
    usuarioId: ObjectId
    prendas: list[ObjectId]
    ocasion: str
    fechaCreacion: datetime