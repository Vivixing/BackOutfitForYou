import datetime
from enums.CategoriaEnums import CategoriaEnums
from pydantic import BaseModel, Field

class TipoPrendaCreadoRequest(BaseModel):
    categoria: CategoriaEnums = Field(...)
    fecha_creacion = Field(default_factory=datetime.datetime.now)

class TipoPrendaActualizadoRequest(BaseModel):
    categoria: CategoriaEnums = Field(...)
    fecha_modificacion = Field(default_factory=datetime.datetime.now)