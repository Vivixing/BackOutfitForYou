from beanie import PydanticObjectId
from models.TipoPrendaModel import TipoPrenda
from repository.TipoPrendaRepository import TipoPrendaRepository

class TipoPrendaService:

    @staticmethod
    async def create_tipo_prenda(new_tipo_prenda: TipoPrenda) -> TipoPrenda:
        return await TipoPrendaRepository.create_tipo_prenda(new_tipo_prenda)
    
    @staticmethod
    async def find_tipo_prenda_by_id(id: PydanticObjectId) -> TipoPrenda:
        try:
            exist_tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_id(id)
            if not exist_tipo_prenda:
                raise Exception("No exite un tipo de prenda con ese ID")
            return exist_tipo_prenda
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_tipo_prenda_by_category(categoria: str) -> TipoPrenda:
        try:
            exist_tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_category(categoria)
            if not exist_tipo_prenda:
                raise Exception("No exite un tipo de prenda con esa categoria")
            return exist_tipo_prenda
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_tipo_prendas() -> list[TipoPrenda]:
        return await TipoPrendaRepository.find_all_tipo_prendas()
    
    @staticmethod
    async def uptade_tipo_prenda(update_tipo_prenda: TipoPrenda) -> TipoPrenda:
        try:
            exist_tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_id(update_tipo_prenda.id)
            if not exist_tipo_prenda:
                raise Exception("No exite un tipo de prenda con ese ID")
            return await TipoPrendaRepository.create_tipo_prenda(update_tipo_prenda)
        except Exception as error:
            raise error