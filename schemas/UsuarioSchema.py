from pydantic import BaseModel, EmailStr

class UsuarioCreadoRequest(BaseModel):
    nombre: str
    email: EmailStr
    contrasena: str

class UsuarioLoginRequest(BaseModel):
    email: EmailStr
    contrasena: str