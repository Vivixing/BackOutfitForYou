from beanie import PydanticObjectId
from schemas.TipoPrendaSchema import TipoPrendaCreadoRequest, TipoPrendaActualizadoRequest
from controllers.TipoPrendaController import TipoPrendaController
from fastapi import APIRouter

routerTipoPrenda = APIRouter(prefix="/type_of_clothing", tags=["TipoPrenda"])

@routerTipoPrenda.post("/create")
async def create_tipo_prenda(request:TipoPrendaCreadoRequest):
    return await TipoPrendaController.create_tipo_prenda(request)

@routerTipoPrenda.get("/get_all")
async def get_all_tipo_prendas():
    return await TipoPrendaController.get_all_tipo_prendas()

@routerTipoPrenda.get("/{tipo_prenda_id}")
async def get_tipo_prenda_by_id(tipo_prenda_id:PydanticObjectId):
    return await TipoPrendaController.get_tipo_prenda_by_id(tipo_prenda_id)

@routerTipoPrenda.put("/update/{tipo_prenda_id}")
async def update_tipo_prenda(id:PydanticObjectId ,request:TipoPrendaActualizadoRequest):
    return await TipoPrendaController.update_tipo_prenda(id, request)

@routerTipoPrenda.get("/get_by_category/{category}")
async def get_tipo_prenda_by_name(category:str):
    return await TipoPrendaController.get_tipo_prenda_by_category(category)
