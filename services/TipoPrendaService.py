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
                raise Exception("El tipo de prenda que buscas no existe.")
            return exist_tipo_prenda
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_tipo_prenda_by_category(categoria: str) -> list[TipoPrenda]:
        try:
            exist_tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_category(categoria)
            if not exist_tipo_prenda:
                raise Exception("No se encontraron tipos de prenda en esta categoría.")
            return exist_tipo_prenda
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_tipo_prendas() -> list[TipoPrenda]:
        try:
            tipo_prendas = await TipoPrendaRepository.find_all_tipo_prendas()
            if not tipo_prendas:
                raise Exception("Aún no hay tipos de prendas registrados.")
            return tipo_prendas
        except Exception as error:
            raise error
    
    @staticmethod
    async def update_tipo_prenda(id: PydanticObjectId, update_data: dict) -> TipoPrenda:
        try:
            exist_tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_id(id)
            if not exist_tipo_prenda:
                raise Exception("No se puede actualizar porque el tipo de prenda no existe.")
            return await TipoPrendaRepository.update_tipo_prenda(id, update_data)
        except Exception as error:
            raise error