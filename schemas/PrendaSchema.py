
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

class PrendaCreadoRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    tipoPrendaId: PydanticObjectId = Field(...)
    nombre: str = Field(..., min_length=3, max_length=30)
    color: Optional[str] = Field(..., min_length=3, max_length=20)
    imagen: str = Field(..., min_length=5, max_length=200)
    fechaCreado = Field(default_factory=datetime.datetime.now)

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

    @field_validator("imagen", mode="before")
    def validar_extension_imagen(cls, cadena_imagen):
        if not cadena_imagen.endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException("Imagen debe de terminar en .png, .jpg o .jpeg")
        if len(cadena_imagen) < 5:
            raise HTTPException("Imagen debe de tener al menos 4 caracteres")
        if len(cadena_imagen) > 200:
            raise HTTPException("Imagen no puede tener más de 200 caracteres")
        return cadena_imagen

class PrendaActualizadoRequest(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=30)
    color: Optional[str] = Field(..., min_length=3, max_length=20)
    fechaActualizado = Field(default_factory=datetime.datetime.now)

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