
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

class PrendaCreadoRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    tipoPrendaId: PydanticObjectId = Field(...)
    nombre: str = Field(...)
    color: Optional[str] = Field(...)
    imagen: str = Field(...)
    fechaCreado = Field(default_factory=datetime.datetime.now)

    @field_validator("imagen")
    def validar_extension_imagen(cls, cadena_imagen):
        if not cadena_imagen.endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException("Imagen debe de terminar en .png, .jpg o .jpeg")
        return cadena_imagen