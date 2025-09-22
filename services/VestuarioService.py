from repository.VestuarioRepository import VestuarioRepository
from models.VestuarioModel import Vestuario
import datetime

class VestuarioService:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        try:            
            return await VestuarioRepository.create_vestuario(vestuario)
        except Exception as error:
            raise error

    @staticmethod
    async def get_vestuario_by_id(vestuario_id: str) -> Vestuario:
        try:
            exist_vestuario = await VestuarioRepository.get_vestuario_by_id(vestuario_id)
            if not exist_vestuario:
                raise Exception("El vestuario que buscas no existe.")
            return exist_vestuario
        except Exception as error:
            raise error

    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: str) -> list[Vestuario]:
        try:
            exist_vestuario_by_usuario = await VestuarioRepository.get_vestuario_by_usuario(usuario_id)
            if not exist_vestuario_by_usuario:
                raise Exception("Este usuario aún no tiene vestuarios registrados.")
            return exist_vestuario_by_usuario
        except Exception as error:
            raise error
