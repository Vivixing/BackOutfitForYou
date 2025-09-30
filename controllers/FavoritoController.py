from services.FavoritoService import FavoritoService
from models.FavoritoModel import Favorito
from beanie import PydanticObjectId
from fastapi import HTTPException
from schemas.FavoritoSchema import FavoritoRequest
from services.UsuarioService import UsuarioService
from services.VestuarioService import VestuarioService
import datetime

class FavoritoController:

    @staticmethod
    async def create_favorito(request: FavoritoRequest):
        try:
            usuario = await UsuarioService.find_user_by_id(request.usuarioId)
            vestuario = await VestuarioService.get_vestuario_by_id(request.vestuarioId)

            favorito_convert = Favorito(
                usuarioId=usuario,
                vestuarioId=vestuario,
                fechaCreado=datetime.datetime.now(),
                estado=True
            )
            favorito = await FavoritoService.create_favorito(favorito_convert)
            return {"message": "Favorito creado exitosamente", "data": favorito}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def get_favoritos_by_usuario(usuarioId: PydanticObjectId):
        print("Llegó al controller", usuarioId)
        try:
            favoritos = await FavoritoService.get_favoritos_by_usuario(usuarioId)
            return {"status": 200, "message": "Favoritos obtenidos exitosamente", "data": favoritos}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    @staticmethod
    async def delete_favorito(favoritoId: PydanticObjectId):
        try:
            favorito_eliminado = await FavoritoService.delete_favorito(favoritoId)
            if favorito_eliminado:
                return {"status": 200, "message": "Favorito eliminado exitosamente", "data": favorito_eliminado}
            else:
                raise HTTPException(status_code=404, detail="Favorito no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        