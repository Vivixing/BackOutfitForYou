from beanie import PydanticObjectId
from models.PrendaModel import Prenda
from schemas.PrendaSchema import PrendaCreadoRequest
from services.PrendaService import PrendaService
from fastapi import HTTPException

class PrendaController:

    @staticmethod
    async def create_prenda(request:PrendaCreadoRequest):
        try:
            prenda_convert = Prenda(**request.dict())  
            prenda = await PrendaService.create_prenda(prenda_convert)
            return {"status": 200, "message": "Prenda creada correctamente", "prenda_id":str(prenda.id), "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    async def get_prenda_by_id(prenda_id:PydanticObjectId):
        try:
            prenda = await PrendaService.find_prenda_by_id(prenda_id)
            return {"status": 200, "message": "Prenda encontrada", "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prendas_by_user(user_id:PydanticObjectId):
        try:
            prendas = await PrendaService.find_prendas_by_user(user_id)
            return {"status": 200, "message": "Prendas encontradas", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prendas_by_tipo_prenda(tipo_prenda_id:PydanticObjectId):
        try:
            prendas = await PrendaService.find_prendas_by_tipo_prenda(tipo_prenda_id)
            return {"status": 200, "message": "Prendas encontradas", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prenda_by_name(name:str):
        try:
            prenda = await PrendaService.find_prenda_by_name(name)
            return {"status": 200, "message": "Prenda encontrada", "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_all_prendas():
        try:
            prendas = await PrendaService.find_all_prendas()
            return {"status": 200, "message": "Prendas encontradas", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def update_prenda(request:PrendaCreadoRequest):
        try:
            prenda_convert = Prenda(**request.dict())  
            prenda = await PrendaService.update_prenda(prenda_convert)
            return {"status": 200, "message": "Prenda actualizada correctamente", "prenda_id":str(prenda.id), "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    async def delete_prenda(prenda_id:PydanticObjectId):
        try:
            prenda = await PrendaService.delete_prenda(prenda_id)
            return {"status": 200, "message": "Prenda eliminada correctamente", "prenda_id":str(prenda.id), "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))