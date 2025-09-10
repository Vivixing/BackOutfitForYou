from controllers.VisualizacionController import VisualizacionController
from fastapi import APIRouter, UploadFile

routerVisualizacion = APIRouter(prefix="/display", tags=["VisualizacionPrueba"])

@routerVisualizacion.post("/tryon")
async def display_outfit(person: UploadFile, garment:list[UploadFile]):
    return await VisualizacionController.mostrarVisualizacionOutfit(person, garment)