from beanie import Document
from pydantic import EmailStr, BaseModel

class UsuarioModel(BaseModel):
    nombre: str
    email: EmailStr
    contrasena: str

    class Settings:
        collection = "usuarios"

class Usuario(UsuarioModel, Document):
    pass