import datetime
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

class PrendaCreadoRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    tipoPrendaId: PydanticObjectId = Field(...)
    nombre: str = Field(..., min_length=3, max_length=30)
    color: str = Field(..., min_length=3, max_length=20)

    @field_validator("nombre", mode="before")
    def validar_nombre(cls, nombre_prenda):
        if not nombre_prenda.replace(" ", "").isalpha():
            raise HTTPException("Nombre de la prenda no puede contener números ni caracteres especiales")
        if len(nombre_prenda) < 3:
            raise HTTPException("Nombre de la prenda debe de tener al menos 4 caracteres")
        if len(nombre_prenda) > 30:
            raise HTTPException("Nombre de la prenda no puede tener más de 30 caracteres")
        return nombre_prenda
    
    @field_validator("color", mode="before")
    def validar_color(cls, color_prenda):
        if not color_prenda.replace(" ", "").isalpha():
            raise HTTPException("Color de la prenda no puede contener números ni caracteres especiales")
        if len(color_prenda) < 3:
            raise HTTPException("Color de la prenda debe de tener al menos 3 caracteres")
        if len(color_prenda) > 20:
            raise HTTPException("Color de la prenda no puede tener más de 20 caracteres")
        return color_prenda
    
class PrendaActualizadoRequest(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=30)
    color: Optional[str] = Field(None, min_length=3, max_length=20)
    fechaModificado: datetime.datetime = Field(default_factory=datetime.datetime.now)

    @field_validator("nombre", mode="before")
    def validar_nombre(cls, nombre_prenda):
        if nombre_prenda is None:
            return nombre_prenda  # Si no se envía, no se valida
        if not nombre_prenda.replace(" ", "").isalpha():
            raise HTTPException(status_code=400, detail="Nombre de la prenda no puede contener números ni caracteres especiales")
        if len(nombre_prenda) < 3:
            raise HTTPException(status_code=400, detail="Nombre de la prenda debe tener al menos 3 caracteres")
        if len(nombre_prenda) > 30:
            raise HTTPException(status_code=400, detail="Nombre de la prenda no puede tener más de 30 caracteres")
        return nombre_prenda
    
    @field_validator("color", mode="before")
    def validar_color(cls, color_prenda):
        if color_prenda is None:
            return color_prenda  # Si no se envía, no se valida
        if not color_prenda.replace(" ", "").isalpha():
            raise HTTPException(status_code=400, detail="Color de la prenda no puede contener números ni caracteres especiales")
        if len(color_prenda) < 3:
            raise HTTPException(status_code=400, detail="Color de la prenda debe tener al menos 3 caracteres")
        if len(color_prenda) > 20:
            raise HTTPException(status_code=400, detail="Color de la prenda no puede tener más de 20 caracteres")
        return color_prenda
