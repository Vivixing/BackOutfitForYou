from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class TipoPrendaModel(BaseModel):
    categoria: str
    fechaCreado: Optional[datetime] = Field(default_factory=datetime.now)
    fechaModificado: Optional[datetime] = Field(default_factory=datetime.now)

    class Settings:
        collection = "tipos_prendas"

class TipoPrenda(TipoPrendaModel, Document):
    pass