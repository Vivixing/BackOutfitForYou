from beanie import PydanticObjectId
from schemas.TipoPrendaSchema import TipoPrendaCreadoRequest, TipoPrendaActualizadoRequest
from controllers.TipoPrendaController import TipoPrendaController
from fastapi import APIRouter

routerTipoPrenda = APIRouter(prefix="/clothes", tags=["Prenda"])

@routerTipoPrenda.post("/create")
async def create_tipo_prenda(request:TipoPrendaCreadoRequest):
    return await TipoPrendaController.create_tipo_prenda(request)

@routerTipoPrenda.get("/{tipo_prenda_id}")
async def get_tipo_prenda_by_id(tipo_prenda_id:PydanticObjectId):
    return await TipoPrendaController.get_tipo_prenda_by_id(tipo_prenda_id)

@routerTipoPrenda.get("/all")
async def get_all_tipo_prendas():
    return await TipoPrendaController.get_all_tipo_prendas()

@routerTipoPrenda.put("/update")
async def update_tipo_prenda(request:TipoPrendaActualizadoRequest):
    return await TipoPrendaController.update_tipo_prenda(request)

@routerTipoPrenda.get("/get-by-category/{category}")
async def get_tipo_prenda_by_name(category:str):
    return await TipoPrendaController.get_tipo_prenda_by_category(category)
