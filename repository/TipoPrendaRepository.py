import datetime
from beanie import PydanticObjectId
from models.TipoPrendaModel import TipoPrenda

class TipoPrendaRepository:

    @staticmethod
    async def create_tipo_prenda(new_tipo_prenda: TipoPrenda) -> TipoPrenda:
        return await new_tipo_prenda.insert()
    
    @staticmethod
    async def update_tipo_prenda(id: PydanticObjectId, update_data: dict) -> TipoPrenda:
            tipo_prenda = await TipoPrendaRepository.find_tipo_prenda_by_id(id)
            if not tipo_prenda:
                return None
            update_data["fechaModificado"] = datetime.datetime.now()
            return await tipo_prenda.update({"$set": update_data})

    @staticmethod
    async def find_tipo_prenda_by_id(id: PydanticObjectId) -> TipoPrenda:
        return await TipoPrenda.get(id)
    
    @staticmethod
    async def find_tipo_prenda_by_category(categoria: str) -> list[TipoPrenda]:
        return await TipoPrenda.find(TipoPrenda.categoria == categoria).to_list()
    
    @staticmethod
    async def find_all_tipo_prendas() -> list[TipoPrenda]:
        return await TipoPrenda.find().to_list()
