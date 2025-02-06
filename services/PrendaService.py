
from models.PrendaModel import Prenda
from repository.PrendaRepository import PrendaRepository
from beanie import PydanticObjectId

class PrendaService:

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await PrendaRepository.create_prenda(new_prenda)
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        try:
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return exist_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> Prenda:
        try: 
            exist_prenda_usuario_id = await PrendaRepository.find_prenda_by_usuario_id(usuario_id)
            if not exist_prenda_usuario_id:
                raise Exception("No existe una prenda con ese usuario ID")
            return exist_prenda_usuario_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> Prenda:
        try:
            exist_prenda_tipo_prenda_id = await PrendaRepository.find_prenda_by_tipo_prenda_id(tipo_prenda_id)
            if not exist_prenda_tipo_prenda_id:
                raise Exception("No existe una prenda con ese tipo de prenda ID")
            return exist_prenda_tipo_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_name(name: str) -> Prenda:
        try: 
            exist_prenda_name = await PrendaRepository.find_prenda_by_name(name)
            if not exist_prenda_name:
                raise Exception("No existe una prenda con ese nombre")
            return exist_prenda_name
        except Exception as error:
            raise error
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Prenda:
        try: 
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return await PrendaRepository.delete_prenda(id)
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_prendas() -> list[Prenda]:
        return await PrendaRepository.find_all_prendas().to_list()
    
    @staticmethod
    async def update_prenda(update_prenda: Prenda) -> Prenda:
        try:
            exist_prenda = await PrendaRepository.find_prenda_by_id(update_prenda.id)
            if not exist_prenda:
                raise Exception("No existe una prenda con ese ID")
            return await PrendaRepository.create_prenda(update_prenda)
        except Exception as error:
            raise error