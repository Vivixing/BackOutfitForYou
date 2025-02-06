from beanie import PydanticObjectId
from fastapi import HTTPException
from services.TipoPrendaService import TipoPrendaService
from schemas.TipoPrendaSchema import TipoPrendaCreadoRequest, TipoPrendaActualizadoRequest
from models.TipoPrendaModel import TipoPrenda

class TipoPrendaController:

    async def create_tipo_prenda(request:TipoPrendaCreadoRequest):
        try:
            tipo_prenda_convert = TipoPrenda(**request.dict())  
            tipo_prenda = await TipoPrendaService.create_tipo_prenda(tipo_prenda_convert)
            return {"status": 200, "message": "Tipo de prenda creado correctamente", "tipo_prenda_id":str(tipo_prenda.id), "data": tipo_prenda}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def get_tipo_prenda_by_id(id:PydanticObjectId):
        try:
            tipo_prenda = await TipoPrendaService.find_tipo_prenda_by_id(id)
            return {"status": 200, "message": "Tipo de prenda encontrado", "data": tipo_prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    async def get_all_tipo_prendas():
        try:
            tipo_prendas = await TipoPrendaService.find_all_tipo_prendas()
            return {"status": 200, "message": "Tipos de prendas encontrados", "data": tipo_prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    async def update_tipo_prenda(request:TipoPrendaActualizadoRequest):
        try:
            tipo_prenda_convert = TipoPrenda(**request.dict())
            tipo_prenda = await TipoPrendaService.uptade_tipo_prenda(tipo_prenda_convert)
            return {"status": 200, "message": "Tipo de prenda actualizado correctamente", "tipo_prenda_id":str(tipo_prenda.id), "data": tipo_prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    async def get_tipo_prenda_by_category(category:str):
        try:
            tipo_prenda = await TipoPrendaService.find_tipo_prenda_by_category(category)
            return {"status": 200, "message": "Tipo de prenda encontrado", "data": tipo_prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))