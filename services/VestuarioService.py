from repository.VestuarioRepository import VestuarioRepository
from models.VestuarioModel import Vestuario

class VestuarioService:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        return await VestuarioRepository.create_vestuario(vestuario)

    @staticmethod
    async def get_vestuario_by_id(vestuario_id: str) -> Vestuario | None:
        return await VestuarioRepository.get_vestuario_by_id(vestuario_id)

    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: str) -> list[Vestuario]:
        return await VestuarioRepository.get_vestuario_by_usuario(usuario_id)
