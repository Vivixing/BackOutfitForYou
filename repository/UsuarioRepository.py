from models.UsuarioModel import Usuario
from beanie import PydanticObjectId
from pydantic import EmailStr


class UsuarioRepository:

    @staticmethod
    async def create_user(new_user: Usuario) -> Usuario:
        return await Usuario.insert(new_user)
    
    @staticmethod
    async def find_user_by_name(name: str) -> Usuario:
        return await Usuario.find_one(Usuario.nombre == name)
    
    @staticmethod
    async def find_user_by_email(email: EmailStr) -> Usuario:
        return await Usuario.find_one(Usuario.email == email)
 
    @staticmethod
    async def find_user_by_id(user_id: PydanticObjectId) -> Usuario:
        return await Usuario.get(user_id)
    