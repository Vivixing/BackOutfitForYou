from typing import Optional
from repository.FavoritoRepository import FavoritoRepository
from repository.UsuarioRepository import UsuarioRepository
from repository.VestuarioRepository import VestuarioRepository
from beanie import PydanticObjectId
from models.FavoritoModel import Favorito
import datetime

class FavoritoService:

    @staticmethod
    async def create_favorito(usuarioId: str, vestuarioId: str) -> Favorito:
        try:
            if not usuarioId:
                raise Exception("El usuario es obligatorio para guardar un favorito.")
            usuario_exist = await UsuarioRepository.find_user_by_id(usuarioId)
            if not usuario_exist:
                raise Exception("El usuario no existe.")
            
            if not vestuarioId:
                raise Exception("El vestuario es obligatorio para guardar un favorito.")
            vestuario_exist = await VestuarioRepository.get_vestuario_by_id(vestuarioId)
            if not vestuario_exist:
                raise Exception("El vestuario no existe.")

            favorito = Favorito(
                usuarioId=usuarioId,
                vestuarioId=vestuarioId,
                fechaCreado= datetime.datetime.now(),
                estado=True
            )
            return await FavoritoRepository.create_favorito(favorito)
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