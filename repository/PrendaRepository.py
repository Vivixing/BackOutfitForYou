from models.PrendaModel import Prenda
from beanie import PydanticObjectId

class PrendaRepository:

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await new_prenda.insert()
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        return await Prenda.find_one(Prenda.id == id)
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> Prenda:
        return await Prenda.find_one(Prenda.usuarioId == usuario_id)
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> Prenda:
        return await Prenda.find_one(Prenda.tipoPrendaId == tipo_prenda_id)
    
    @staticmethod
    async def find_prenda_by_name(name: str) -> Prenda:
        return await Prenda.find_one(Prenda.nombre == name)
    
    @staticmethod
    async def find_all_prendas() -> list[Prenda]:
        return await Prenda.all().to_list()
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> None:
        return await Prenda.delete_one(Prenda.id == id)
    