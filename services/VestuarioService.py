from repository.VestuarioRepository import VestuarioRepository
from models.VestuarioModel import Vestuario
from repository.UsuarioRepository import UsuarioRepository
from repository.PrendaRepository import PrendaRepository
import datetime

class VestuarioService:

    @staticmethod
    async def create_vestuario(vestuario: Vestuario) -> Vestuario:
        try:
            if not vestuario.usuarioId:
                raise Exception("El usuario es obligatorio para crear un vestuario.")
            exist_usuario = await UsuarioRepository.find_user_by_id(vestuario.usuarioId)
            if not exist_usuario:
                raise Exception("El usuario no existe.")
            
            if not vestuario.prendas or len(vestuario.prendas) == 0:
                raise Exception("El vestuario debe contener prendas.")
            if len(vestuario.prendas) != 2:
                raise Exception("El vestuario debe contener exactamente 2 prendas.")
            
            for ref in vestuario.prendas:
                prenda_id = str(ref.id)
                prenda = await PrendaRepository.find_prenda_by_id(prenda_id)
                if not prenda:
                    raise Exception(f"La prenda con ID {prenda_id} no existe.")
                if prenda.usuarioId != vestuario.usuarioId:
                    raise Exception(f"La prenda con ID {prenda_id} no pertenece al usuario.")
            
            if not vestuario.fechaCreado:
                vestuario.fechaCreado = datetime.datetime.now()

            return await VestuarioRepository.create_vestuario(vestuario)
        except Exception as error:
            raise error

    @staticmethod
    async def get_vestuario_by_id(vestuario_id: str) -> Vestuario:
        try:
            exist_vestuario = await VestuarioRepository.get_vestuario_by_id(vestuario_id)
            if not exist_vestuario:
                raise Exception("El vestuario que buscas no existe.")
            return exist_vestuario
        except Exception as error:
            raise error

    @staticmethod
    async def get_vestuario_by_usuario(usuario_id: str) -> list[Vestuario]:
        try:
            exist_vestuario_by_usuario = await VestuarioRepository.get_vestuario_by_usuario(usuario_id)
            if not exist_vestuario_by_usuario:
                raise Exception("Este usuario aún no tiene vestuarios registrados.")
            return exist_vestuario_by_usuario
        except Exception as error:
            raise error
