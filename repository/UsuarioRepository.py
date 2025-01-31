from models.UsuarioModel import Usuario
from beanie import PydanticObjectId

class UsuarioRepository:

    @staticmethod
    async def create_user(new_user: Usuario) -> Usuario:
        return await new_user.insert()
    
    @staticmethod
    async def find_user_by_email(email: str) -> Usuario:
        return await Usuario.find_one(Usuario.email == email)
    
    @staticmethod
    async def find_user_by_id(user_id: PydanticObjectId) -> Usuario:
        return await Usuario.get(user_id)
    