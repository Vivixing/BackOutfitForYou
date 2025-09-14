from typing import Optional
from repository.FavoritoRepository import FavoritoRepository
from beanie import PydanticObjectId
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
    async def get_favoritos_by_usuario(usuarioId: PydanticObjectId) -> list[Favorito]:
        try:
            exist_favorito_usuario_id = await FavoritoRepository.get_favoritos_by_usuario(usuarioId)
            if not exist_favorito_usuario_id:
                raise Exception ('No existen vestuarios favoritos para este usuario')
            return exist_favorito_usuario_id
        except Exception as error:
            raise error
        
    @staticmethod
    async def delete_favorito(favoritoId: PydanticObjectId) -> Optional[Favorito]:
        try:
            exist_favorito_id = await FavoritoRepository.delete_favorito(favoritoId)
            if not exist_favorito_id:
                raise Exception("No existe un favorito con ese ID o ya ha sido eliminado")
            return exist_favorito_id
        except Exception as error:
            raise error