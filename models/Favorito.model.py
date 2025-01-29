from pydantic import BaseModel, ObjectId
from datetime import datetime

class Favorito(BaseModel):
    _id: ObjectId
    usuarioId: ObjectId
    vestuarioId: ObjectId
    fechaCreado: datetime