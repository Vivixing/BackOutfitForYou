from models.VestuarioModel import Vestuario

class VestuarioRepository:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        return await Vestuario.insert(vestuario)
    