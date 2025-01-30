from beanie import Document
from typing import Optional

class TipoPrenda(Document):
    tipo: str
    categoria: Optional[str]

    class Settings:
        collection = "tipos_prendas"