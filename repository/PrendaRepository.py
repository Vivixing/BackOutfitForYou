import datetime 
from typing import Optional 
from models.PrendaModel import Prenda
from beanie import PydanticObjectId

class PrendaRepository:

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await Prenda.insert(new_prenda)
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        return await Prenda.get(id)
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> list[Prenda]:
        return await Prenda.find(Prenda.usuarioId.id == usuario_id).to_list()
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> list[Prenda]:
        return await Prenda.find(Prenda.tipoPrendaId.id == tipo_prenda_id).to_list()
    
    @staticmethod
    async def find_prenda_by_name(name: str) -> list[Prenda]:
        return await Prenda.find(Prenda.nombre == name).to_list()
    
    @staticmethod
    async def find_all_prendas() -> list[Prenda]:
        return await Prenda.find(Prenda.estado == True).to_list()
    
    @staticmethod
    async def update_prenda(id:PydanticObjectId, update_prenda:dict) -> Prenda:
        prenda = await PrendaRepository.find_prenda_by_id(id)
        return await prenda.update({"$set":update_prenda})
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Optional[Prenda]:
        prenda_a_eliminar = await Prenda.find_one(Prenda.id == id, Prenda.estado == True)

        if prenda_a_eliminar:
            return await prenda_a_eliminar.set({"estado": False, "fechaModificado": datetime.datetime.now()})
        return None