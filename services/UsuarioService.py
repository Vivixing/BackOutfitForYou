from models.UsuarioModel import Usuario
from repository.UsuarioRepository import UsuarioRepository
from beanie import PydanticObjectId
from pydantic import EmailStr

class UsuarioService:
    
    @staticmethod
    async def create_user(new_user: Usuario) -> Usuario:
        exist_name = await UsuarioRepository.find_user_by_name(new_user.nombre)   
        if exist_name:
            raise Exception("Ya existe un usuario con ese nombre")
        exist_email = await UsuarioRepository.find_user_by_email(new_user.email)
        if exist_email:
            raise Exception("El usuario ya está registrado")
        return await UsuarioRepository.create_user(new_user)
    
    @staticmethod
    async def find_user_by_email(email: EmailStr) -> Usuario:
        exist_email_user = await UsuarioRepository.find_user_by_email(email)
        if not exist_email_user:
            raise Exception("No exite un usuario con ese email")
        return exist_email_user
    
    @staticmethod
    async def find_user_by_id(user_id: PydanticObjectId) -> Usuario:
        exist_user_id = await UsuarioRepository.find_user_by_id(user_id)
        if not exist_user_id:
            raise Exception("No exite un usuario con ese ID")
        return exist_user_id
    
    @staticmethod
    async def login_user(email: EmailStr, password: str) -> Usuario:
        exist_user_login = await UsuarioRepository.find_user_by_email(email)
        if not exist_user_login:
            raise Exception("No exite un usuario con ese email")
        if exist_user_login.contrasena != password:
            raise Exception("Contraseña incorrecta")
        return exist_user_login