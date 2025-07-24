from fastapi import APIRouter
from controllers.RecomendacionController import RecomendacionController
from schemas.RecomendacionSchema import RecomendacionRequest, RecomendacionResponse

routerRecomendacion = APIRouter(prefix="/recomendation", tags=["Recomendacion"])

@routerRecomendacion.post("/recomendation_clothe")
async def crear_recomendacion_vestimenta(request:RecomendacionRequest):
    return await RecomendacionController.crear_recomendacion(request)
