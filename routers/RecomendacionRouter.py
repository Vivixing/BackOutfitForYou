from fastapi import APIRouter
from controllers.RecomendacionController import RecomendacionController
from schemas.RecomendacionSchema import RecomendacionRequest, RecomendacionResponse

routerRecomendacion = APIRouter(prefix="/recomendation", tags=["Recomendacion"])

@routerRecomendacion.post("/recomendation_clothe")
async def recomendacion_vestimenta(request:RecomendacionRequest):
    return await RecomendacionController.generar_recomendacion(request.usuarioId, request.ocasion)

@routerRecomendacion.post("/create")
async def save_recomendation(request:RecomendacionRequest):
    return await RecomendacionController.guardar_recomendacion(request.usuarioId, request.ocasion, request.vestuarioSugerido)
