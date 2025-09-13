from controllers.VisualizacionController import VisualizacionController
from schemas.VisualizacionSchema import VisualizacionCreateRequest
from fastapi import APIRouter, UploadFile

routerVisualizacion = APIRouter(prefix="/display", tags=["VisualizacionPrueba"])

@routerVisualizacion.post("/tryon")
async def display_outfit(person: UploadFile, garment:list[UploadFile]):
    return await VisualizacionController.mostrarVisualizacionOutfit(person, garment)

@routerVisualizacion.post("/create")
async def create_visualizacion(request: VisualizacionCreateRequest):
    return await VisualizacionController.guardarVisualizacionOutfit(request.usuarioId, request.vestuarioId, request.imagen_visualizacion)