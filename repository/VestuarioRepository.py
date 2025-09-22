from models.VestuarioModel import Vestuario

class VestuarioRepository:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        return await Vestuario.insert(vestuario)
    
    @staticmethod
    async def get_vestuario_by_id(vestuario_id: str) -> Vestuario | None:
        return await Vestuario.get(vestuario_id, fetch_links=True)
    
    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: str) -> list[Vestuario]:
        return await Vestuario.find(Vestuario.usuarioId == usuario_id, fetch_links=True).to_list()
    