import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException 
from enums.CategoriaEnums import CategoriaEnums
from pydantic import BaseModel, Field, field_validator

class TipoPrendaCreadoRequest(BaseModel):
    categoria: str = Field(...)
    fecha_creacion: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @field_validator("categoria")
    def validate_categoria(cls, value):
        categorias_validas = {e.value for e in CategoriaEnums}
        if value not in categorias_validas:
            raise HTTPException(status_code=422, detail=f"Categoría inválida: '{value}'. Debe ser una de {categorias_validas}")
        return value

class TipoPrendaActualizadoRequest(BaseModel):
    categoria: str = Field(...)
    fecha_modificacion: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @field_validator("categoria")
    def validate_categoria(cls, value):
        categorias_validas = {e.value for e in CategoriaEnums}
        if value not in categorias_validas:
            raise HTTPException(status_code=422, detail=f"Categoría inválida: '{value}'. Debe ser una de {categorias_validas}")
        return value
