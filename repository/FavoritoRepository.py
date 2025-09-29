from typing import Optional
from beanie import PydanticObjectId
from models.FavoritoModel import Favorito

class FavoritoRepository:

    @staticmethod
    async def create_favorito(favorito: Favorito) -> Favorito:
        return await Favorito.insert(favorito)
    
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: PydanticObjectId) -> list[Favorito]:
        print("Repository - tipo de usuarioId:", type(usuarioId), usuarioId)
        query = Favorito.find(Favorito.usuarioId.id == usuarioId, Favorito.estado == True, fetch_links=True)
        print("Query:", query)
        return await query.to_list()
    
    @staticmethod
    async def delete_favorito(favoritoId: PydanticObjectId) -> Optional[Favorito]:
        favorito_a_eliminar = await Favorito.find_one(Favorito.id == favoritoId, Favorito.estado == True)
        if favorito_a_eliminar:
            return await favorito_a_eliminar.set({"estado": False})
        return None