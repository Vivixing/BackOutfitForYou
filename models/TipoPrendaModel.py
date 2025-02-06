from datetime import datetime
from beanie import Document
from pydantic import BaseModel

class TipoPrendaModel(BaseModel):
    categoria: str
    fechaCreado: datetime
    fechaModificado: datetime

    class Settings:
        collection = "tipos_prendas"

class TipoPrenda(TipoPrendaModel, Document):
    pass