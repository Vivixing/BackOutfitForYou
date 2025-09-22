from services.VestuarioService import VestuarioService
from models.VestuarioModel import Vestuario
from beanie import PydanticObjectId
from fastapi import HTTPException


class VestuarioController:
    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        vestuario_creado = await VestuarioService.create_vestuario(vestuario)
        return {"message": "Vestuario creado", "data":vestuario_creado}


    @staticmethod
    async def get_vestuario_by_id(vestuario_id: PydanticObjectId) -> Vestuario:
        try: 
            vestuario = await VestuarioService.get_vestuario_by_id(vestuario_id)
            return {"message": "Vestuario encontrado", "data":vestuario}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))


    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: PydanticObjectId) -> list[Vestuario]:
        try:
            Vestuario_user = await VestuarioService.get_vestuario_by_usuario(usuario_id)
            return {"message":"Vestuario encontrado", "data": Vestuario_user}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))