import datetime
import re
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from typing import Literal

hex_pattern = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"

class PrendaCreadoRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    tipoPrendaId: PydanticObjectId = Field(...)
    nombre: str = Field(..., min_length=3, max_length=30)
    color: str = Field(..., min_length=3, max_length=20)
    imagen_base64: str = Field(...)

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

        if color_prenda is None:
            return color_prenda
        
        if not isinstance(color_prenda, str):
            raise HTTPException(status_code=400, detail="El color debe ser una cadena de texto")
        
        if not re.match(hex_pattern, color_prenda):
            raise HTTPException(
                status_code=400,
                detail="Color debe estar en formato de código hexadecimal"
            )
        return color_prenda
    
    @field_validator("imagen_base64", mode="before")
    def validar_base64(cls,valor):
        if valor is not None and not isinstance(valor, str):
            raise HTTPException("El campo imagen_base64 debe ser una cadena en base64")
        return valor
    
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
            return color_prenda
        
        if not isinstance(color_prenda, str):
            raise HTTPException(status_code=400, detail="El color debe ser una cadena de texto")
        
        if not re.match(hex_pattern, color_prenda):
            raise HTTPException(
                status_code=400,
                detail="Color debe estar en formato de código hexadecimal"
            )
        return color_prenda


class Clothing(BaseModel):
    hay_prenda: bool = Field(..., description="Whether this image is a clothing item")
    tipo_prenda: str = Field(..., description="Type of clothing (only in English)")
    zona_cuerpo: Literal["superior", "inferior"] = Field(
        ..., description="Body area: 'superior' or 'inferior'")