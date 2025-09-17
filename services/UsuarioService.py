from models.UsuarioModel import Usuario
from repository.UsuarioRepository import UsuarioRepository
from beanie import PydanticObjectId
from pydantic import EmailStr


class UsuarioService:
    
    @staticmethod
    async def create_user(new_user: Usuario) -> Usuario:
        try: 
            exist_name = await UsuarioRepository.find_user_by_name(new_user.nombre)   
            if exist_name:
                raise Exception("El nombre de usuario ya está en uso. Por favor, elige otro.")
            exist_email = await UsuarioRepository.find_user_by_email(new_user.email)
            if exist_email:
                raise Exception("Este correo ya está registrado. Intenta iniciar sesión.")
            return await UsuarioRepository.create_user(new_user)
        except Exception as error:
            raise error
        
    @staticmethod
    async def find_user_by_email(email: EmailStr) -> Usuario:
        try:
            exist_email_user = await UsuarioRepository.find_user_by_email(email)
            if not exist_email_user:
                raise Exception("No se encontró ningún usuario con ese correo.")
            return exist_email_user
        except Exception as error:
            raise error
        
    @staticmethod
    async def find_user_by_id(user_id: PydanticObjectId) -> Usuario:
        try:
            exist_user_id = await UsuarioRepository.find_user_by_id(user_id)
            if not exist_user_id:
                raise Exception("El usuario que buscas no existe.")
            return exist_user_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def login_user(email: EmailStr, password: str) -> Usuario:
        try: 
            exist_user_login = await UsuarioRepository.find_user_by_email(email)
            if not exist_user_login or exist_user_login.contrasena != password:
                raise Exception("El correo o la contraseña no son correctos.")
            return exist_user_login
        except Exception as error:
            raise error