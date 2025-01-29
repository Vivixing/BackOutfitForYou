from pydantic import BaseModel, EmailStr, ObjectId

class Usuario(BaseModel):
    _id: ObjectId
    nombre: str
    email: EmailStr
    contrasena: str
    closet: list[ObjectId]
    favoritos: list[ObjectId]
