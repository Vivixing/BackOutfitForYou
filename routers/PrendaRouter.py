from typing import List
from beanie import PydanticObjectId
from controllers.PrendaController import PrendaController
from schemas.PrendaSchema import PrendaActualizadoRequest, PrendaCreadoRequest
from fastapi import APIRouter, File, UploadFile

routerPrenda = APIRouter(prefix="/clothe", tags=["Prenda"])

@routerPrenda.post("/predict_clothe")
async def predict_prenda(imagen: UploadFile = File(...)):
    return await PrendaController.predict_prenda(imagen)

@routerPrenda.post("/create")
async def create_prenda(request: PrendaCreadoRequest):
    return await PrendaController.create_prenda(request)

@routerPrenda.get("/get_by_id/{prenda_id}")
async def get_prenda_by_id(prenda_id:PydanticObjectId):
    return await PrendaController.get_prenda_by_id(prenda_id)

@routerPrenda.patch("/update/{prenda_id}")
async def update_prenda(prenda_id:PydanticObjectId, request:PrendaActualizadoRequest):
    return await PrendaController.update_prenda(prenda_id, request)

@routerPrenda.get("/get_by_user/{user_id}")
async def get_prenda_by_user(user_id:PydanticObjectId):
    return await PrendaController.get_prendas_by_user(user_id)

@routerPrenda.get("/get_by_type/{tipo_prenda_id}")
async def get_prenda_by_tipo_prenda(tipo_prenda_id:PydanticObjectId):
    return await PrendaController.get_prendas_by_tipo_prenda(tipo_prenda_id)

@routerPrenda.get("/get_by_name/{name}")
async def get_prenda_by_name(name:str):
    return await PrendaController.get_prenda_by_name(name)

@routerPrenda.delete("/delete/{prenda_id}")
async def delete_prenda(prenda_id:PydanticObjectId):
    return await PrendaController.delete_prenda(prenda_id)