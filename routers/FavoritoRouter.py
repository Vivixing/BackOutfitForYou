from controllers.FavoritoController import FavoritoController
from beanie import PydanticObjectId
from fastapi import APIRouter

routerFavorito = APIRouter(prefix="/favorite", tags=["Favorito"])

@routerFavorito.post("create", response_model=dict)
async def create_favorito(usuarioId: PydanticObjectId, vestuarioId: list[PydanticObjectId]):
    return await FavoritoController.create_favorito(usuarioId, vestuarioId)

@routerFavorito.get("/{usuarioId}", response_model=dict)
async def get_favoritos_by_usuario(usuarioId: PydanticObjectId):
    return await FavoritoController.get_favoritos_by_usuario(usuarioId)