import datetime 
from typing import Optional, List
from models.PrendaModel import Prenda
from beanie import PydanticObjectId

class PrendaRepository:

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await Prenda.insert(new_prenda)
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        return await Prenda.get(id, fetch_links=True)
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> list[Prenda]:
        return await Prenda.find(Prenda.usuarioId.id == usuario_id, fetch_links=True).to_list()
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> list[Prenda]:
        return await Prenda.find(Prenda.tipoPrendaId.id == tipo_prenda_id, fetch_links=True).to_list()
    
    @staticmethod
    async def find_prenda_by_imagen_usuario(usuario_id: PydanticObjectId, imagen_base64: str) -> Optional[Prenda]:
        return await Prenda.find_one(
            {"usuario_id": usuario_id, "imagen_base64": imagen_base64}, fetch_links=True
        )

    @staticmethod
    async def find_prenda_by_name(name: str) -> list[Prenda]:
        return await Prenda.find(Prenda.nombre == name, fetch_links=True).to_list()
    
    @staticmethod
    async def find_all_prendas() -> List[Prenda]:
        return await Prenda.find(Prenda.estado == True, fetch_links=True).to_list()

    @staticmethod
    async def update_prenda(id:PydanticObjectId, update_prenda:dict) -> Prenda:
        prenda = await PrendaRepository.find_prenda_by_id(id)
        if not prenda:
            return None
        # Agregar fecha de modificación al update
        update_prenda["fechaModificado"] = datetime.datetime.now()

        return await prenda.update({"$set": update_prenda})
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Optional[Prenda]:
        prenda_a_eliminar = await Prenda.find_one(Prenda.id == id, Prenda.estado == True)

        if prenda_a_eliminar:
            return await prenda_a_eliminar.set({"estado": False, "fechaModificado": datetime.datetime.now()})
        return None