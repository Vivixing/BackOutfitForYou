from pydantic  import BaseModel, ObjectId
from datetime import datetime

class Recomendacion(BaseModel):
    _id: ObjectId
    usuarioId: ObjectId
    ocasion: str
    vestuarioSugerido: list[ObjectId]
    fechaCreado: datetime