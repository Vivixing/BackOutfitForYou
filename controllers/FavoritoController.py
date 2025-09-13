from services.FavoritoService import FavoritoService
from models.FavoritoModel import Favorito
from beanie import PydanticObjectId
from fastapi import HTTPException

class FavoritoController:

    @staticmethod
    async def create_favorito(usuarioId: PydanticObjectId, vestuarioId: list[PydanticObjectId]) -> Favorito:
        try:
            favorito = await FavoritoService.create_favorito(usuarioId, vestuarioId)
            return {"message": "Favorito creado exitosamente", "data": favorito}
        except Exception as e:
             raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: PydanticObjectId) -> list[Favorito]:
        try:
            favoritos = await FavoritoService.get_favoritos_by_usuario(usuarioId)
            return {"message": "Favoritos obtenidos exitosamente", "data": favoritos}
        except Exception as e:
             raise HTTPException(status_code=500, detail=str(e))
        