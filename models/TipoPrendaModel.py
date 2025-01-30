from beanie import Document
from typing import Optional
from pydantic import BaseModel

class TipoPrendaModel(BaseModel):
    tipo: str
    categoria: Optional[str]

    class Settings:
        collection = "tipos_prendas"

class TipoPrenda(TipoPrendaModel, Document):
    pass