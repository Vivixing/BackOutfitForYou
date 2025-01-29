from pydantic import BaseModel, ObjectId
from datetime import datetime
from typing import Optional

class Prenda(BaseModel):
    _id: ObjectId
    usuarioId: ObjectId
    tipoPrendaId: ObjectId
    nombre: str
    color: Optional[str]
    imagen: str
    fechaCreado: datetime
    fechaModificado: datetime