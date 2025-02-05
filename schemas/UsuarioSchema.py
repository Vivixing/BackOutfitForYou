from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioCreadoRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    contrasena: str

    @field_validator("nombre", mode="before")
    def nombre_validator(cls, value):
        if not value.replace(" ", "").isalpha():
            raise HTTPException(status_code=422, detail="El nombre no puede contener números ni caracteres especiales")
        if len(value) < 2:
            raise HTTPException(status_code=422, detail="El nombre debe tener al menos 2 caracteres")
        if len(value) > 30:
            raise HTTPException(status_code=422, detail="El nombre no puede tener más de 30 caracteres")
        return value

class UsuarioLoginRequest(BaseModel):
    email: EmailStr
    contrasena: str

