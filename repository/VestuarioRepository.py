from beanie import PydanticObjectId
from models.VestuarioModel import Vestuario

class VestuarioRepository:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        return await Vestuario.insert(vestuario)
    
    @staticmethod
    async def get_vestuario_by_id(vestuario_id: PydanticObjectId) -> Vestuario:
        return await Vestuario.get(vestuario_id, fetch_links=True)
    
    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: PydanticObjectId) -> list[Vestuario]:
        return await Vestuario.find(Vestuario.usuarioId.id == usuario_id, fetch_links=True).to_list()
    