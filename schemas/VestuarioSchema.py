from typing import List
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, model_validator

class VestuarioRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    prendas: List[str] = Field(..., min_items=1, description="Debe incluir al menos una prenda")

    @model_validator(mode='after')
    @classmethod
    def validar_modelo_completo(cls, modelo):
        if modelo.usuarioId and len(modelo.prendas) == 0:
            raise ValueError('Debe haber al menos una prenda registrada para el vestuario.')
        return modelo