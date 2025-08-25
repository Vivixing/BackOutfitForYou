from beanie import PydanticObjectId
from fastapi import APIRouter
from controllers.RecomendacionController import RecomendacionController
from schemas.RecomendacionSchema import RecomendacionRequest

routerRecomendacion = APIRouter(prefix="/recomendation", tags=["Recomendacion"])

@routerRecomendacion.post("/generate_recomendation/{user_id}")
async def recomendacion_vestimenta(user_id:PydanticObjectId, recomendacion: RecomendacionRequest):
    return await RecomendacionController.generar_recomendacion(user_id, recomendacion.ocasion)

@routerRecomendacion.post("/save_recomendation/{user_id}")
async def guardar_recomendacion(user_id:PydanticObjectId, recomendacion: RecomendacionRequest):
    return await RecomendacionController.guadar_recomendacion(user_id, recomendacion.ocasion)