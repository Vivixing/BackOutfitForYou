from typing import Optional
from repository.FavoritoRepository import FavoritoRepository
from beanie import PydanticObjectId
from models.FavoritoModel import Favorito

class FavoritoService:

    @staticmethod
    async def create_favorito(new_favorito) -> Favorito:
        try:
            return await FavoritoRepository.create_favorito(new_favorito)
        except Exception as error:
            raise error
    
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: PydanticObjectId) -> list[Favorito]:
        try:
            exist_favorito_usuario_id = await FavoritoRepository.get_favoritos_by_usuario(usuarioId)
            if not exist_favorito_usuario_id:
                raise Exception ("Aún no tienes vestuarios marcados como favoritos.")
            return exist_favorito_usuario_id
        except Exception as error:
            raise error
        
    @staticmethod
    async def delete_favorito(favoritoId: PydanticObjectId) -> Optional[Favorito]:
        try:
            exist_favorito_id = await FavoritoRepository.delete_favorito(favoritoId)
            if not exist_favorito_id:
                raise Exception("El favorito que intentas eliminar no existe o ya fue eliminado.")
            return exist_favorito_id
        except Exception as error:
            raise error