from controllers.FavoritoController import FavoritoController
from schemas.FavoritoSchema import FavoritoRequest
from beanie import PydanticObjectId
from fastapi import APIRouter

routerFavorito = APIRouter(prefix="/favorite", tags=["Favorito"])

@routerFavorito.post("/create",)
async def create_favorito(request: FavoritoRequest):
    return await FavoritoController.create_favorito(request.usuarioId, request.vestuarioId)

@routerFavorito.get("/{usuarioId}",)
async def get_favoritos_by_usuario(usuarioId: PydanticObjectId):
    return await FavoritoController.get_favoritos_by_usuario(usuarioId)