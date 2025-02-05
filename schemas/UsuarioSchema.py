from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioCreadoRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=30)
    email: EmailStr = Field(...)
    contrasena: str = Field(..., pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]$", min_length=8, max_length=30)

    @field_validator("nombre", mode="before")
    def nombre_validator(cls, value):
        if not value.replace(" ", "").isalpha():
            raise HTTPException(status_code=422, detail="El nombre no puede contener números ni caracteres especiales")
        if len(value) < 2:
            raise HTTPException(status_code=422, detail="El nombre debe tener al menos 2 caracteres")
        if len(value) > 30:
            raise HTTPException(status_code=422, detail="El nombre no puede tener más de 30 caracteres")
        return value

    @field_validator("email", mode="before")
    def email_validator(cls, value):
        if " " in value:
            raise HTTPException(status_code=422, detail="El email no debe contener espacios")
        return value.strip().lower()

    @field_validator("contrasena", mode="before")
    def contrasena_validator(cls, value):
        if not any(char.isupper() for char in value):
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos una letra mayúscula")
        if not any(char.islower() for char in value):
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos una letra minúscula")
        if not any(char.isdigit() for char in value):
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos un número")
        if not any(char in ["@", "$", "!", "%", "*", "?", "&"] for char in value):
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos un caracter especial")
        if len(value) < 8:
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos 8 caracteres")
        if len(value) > 30:
            raise HTTPException(status_code=422, detail="La contraseña no puede tener más de 30 caracteres")
        return value

class UsuarioLoginRequest(BaseModel):
    email: EmailStr = Field(...)
    contrasena: str = Field(..., min_length=8, max_length=30)

    @field_validator("email", mode="before")
    def email_validator(cls, value):
        if " " in value:
            raise HTTPException(status_code=422, detail="El email no debe contener espacios")
        return value.strip().lower()
    
    @field_validator("contrasena", mode="before")
    def contrasena_validator(cls, value):
        if len(value) < 8:
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos 8 caracteres")
        if len(value) > 30:
            raise HTTPException(status_code=422, detail="La contraseña no puede tener más de 30 caracteres")
        return value

