from beanie import PydanticObjectId
from models.TipoPrendaModel import TipoPrenda

class TipoPrendaRepository:

    @staticmethod
    async def create_tipo_prenda(new_tipo_prenda: TipoPrenda) -> TipoPrenda:
        return await new_tipo_prenda.insert()
    
    @staticmethod
    async def find_tipo_prenda_by_id(id: PydanticObjectId) -> TipoPrenda:
        return await TipoPrenda.find_one(TipoPrenda.id == id)
    
    @staticmethod
    async def find_tipo_prenda_by_category(categoria: str) -> TipoPrenda:
        return await TipoPrenda.find_one(TipoPrenda.categoria == categoria)
    
    @staticmethod
    async def find_all_tipo_prendas() -> list[TipoPrenda]:
        return await TipoPrenda.all().to_list()
