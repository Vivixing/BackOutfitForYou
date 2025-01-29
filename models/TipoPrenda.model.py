from pydantic import BaseModel, ObjectiId
from typing import Optional

class TipoPrendaModel(BaseModel):
    _id: ObjectiId
    tipo: str
    categoria: Optional[str]