
import datetime
from pydantic import BaseModel, Field, field_validator


class TipoPrendaCreadoRequest(BaseModel):
    categoria: str = Field(..., min_length=2, max_length=30)
    fecha_creacion = datetime.datetime.now()

class TipoPrendaActualizadoRequest(BaseModel):
    categoria: str = Field(..., min_length=2, max_length=30)
    fecha_modificacion = datetime.datetime.now()