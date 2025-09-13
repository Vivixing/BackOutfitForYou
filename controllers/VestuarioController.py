from services.VestuarioService import VestuarioService
from models.VestuarioModel import Vestuario
from beanie import PydanticObjectId
from fastapi import HTTPException


class VestuarioController:
    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        return await VestuarioService.create_vestuario(vestuario)

    @staticmethod
    async def get_vestuario_by_id(vestuario_id: PydanticObjectId) -> Vestuario:
        vestuario = await VestuarioService.get_vestuario_by_id(vestuario_id)
        if not vestuario:
            raise HTTPException(status_code=404, detail="Vestuario no encontrado")
        return vestuario

    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: PydanticObjectId) -> list[Vestuario]:
        Vestuario_user = await VestuarioService.get_vestuario_by_usuario(usuario_id)
        if not Vestuario_user:
            raise HTTPException(status_code=404, detail="No se encontraron vestuarios de este usuario")
        return Vestuario_user