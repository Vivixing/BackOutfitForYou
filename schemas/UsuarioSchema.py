from pydantic import BaseModel, EmailStr, Field

class UsuarioCreadoRequest(BaseModel):
    nombre: str = Field(..., pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$", min_length=2, max_length=30)
    email: EmailStr
    contrasena: str

class UsuarioLoginRequest(BaseModel):
    email: EmailStr
    contrasena: str
