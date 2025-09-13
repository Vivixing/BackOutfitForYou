from repository.FavoritoRepository import FavoritoRepository
from models.FavoritoModel import Favorito
import datetime

class FavoritoService:

    @staticmethod
    async def create_favorito(usuarioId: str, vestuarioId: str) -> Favorito:

        favorito = Favorito(
            usuarioId=usuarioId,
            vestuarioId=vestuarioId,
            fechaCreado= datetime.datetime.now(),
            estado=True
        )
        return await FavoritoRepository.create_favorito(favorito)
    
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: str) -> list[Favorito]:
        return await FavoritoRepository.get_favoritos_by_usuario(usuarioId)