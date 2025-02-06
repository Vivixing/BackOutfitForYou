from beanie import PydanticObjectId
from fastapi import HTTPException
from services.TipoPrendaService import TipoPrendaService
from schemas.TipoPrendaSchema import TipoPrendaCreadoRequest, TipoPrendaActualizadoRequest
from models.TipoPrendaModel import TipoPrenda

class TipoPrendaController:

    async def create_tipo_prenda(request:TipoPrendaCreadoRequest):
        try:
            #Convertir el request de un BaseModel a un objeto de tipo TipoPrenda (Document)
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