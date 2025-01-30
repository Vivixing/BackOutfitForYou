from beanie import Document, Link
from datetime import datetime
from typing import Optional
from models.UsuarioModel import Usuario
from models.TipoPrendaModel import TipoPrenda

class Prenda(Document):
    usuarioId: Link[Usuario]
    tipoPrendaId: Link[TipoPrenda]
    nombre: str
    color: Optional[str]
    imagen: str
    fechaCreado: datetime
    fechaModificado: datetime

    class Settings:
        collection = "prendas"