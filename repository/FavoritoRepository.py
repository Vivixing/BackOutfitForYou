from models.FavoritoModel import Favorito

class FavoritoRepository:

    @staticmethod
    async def create_favorito(favorito: Favorito) -> Favorito:
        return await Favorito.insert(favorito)
    
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: str) -> list[Favorito]:
        return await Favorito.find(Favorito.usuarioId == usuarioId).to_list()