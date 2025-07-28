from beanie import PydanticObjectId
from fastapi import APIRouter
from controllers.RecomendacionController import RecomendacionController

routerRecomendacion = APIRouter(prefix="/recomendation", tags=["Recomendacion"])

@routerRecomendacion.post("/recomendation_clothe/{user_id}")
async def recomendacion_vestimenta(user_id:PydanticObjectId, ocasion: str):
    return await RecomendacionController.generar_recomendacion(user_id, ocasion)