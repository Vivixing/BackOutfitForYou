from models.UsuarioModel import Usuario
from repository.UsuarioRepository import UsuarioRepository
from beanie import PydanticObjectId

class UsuarioService:
    
    @staticmethod
    async def create_user(new_user: Usuario) -> Usuario:
        return await UsuarioRepository.create_user(new_user)
    
    @staticmethod
    async def find_user_by_email(email: str) -> Usuario:
        exist_user = await UsuarioRepository.find_user_by_email(email)
        if not exist_user:
            raise Exception("No exite un usuario con ese email")
        return exist_user
    
    @staticmethod
    async def find_user_by_id(user_id: PydanticObjectId) -> Usuario:
        exist_user = await UsuarioRepository.find_user_by_id(user_id)
        print(exist_user)
        if not exist_user:
            raise Exception("No exite un usuario con ese id")
        return exist_user