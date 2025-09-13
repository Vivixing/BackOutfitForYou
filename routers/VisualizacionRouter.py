from beanie import PydanticObjectId
from controllers.VisualizacionController import VisualizacionController
from fastapi import APIRouter, UploadFile

routerVisualizacion = APIRouter(prefix="/display", tags=["VisualizacionPrueba"])

@routerVisualizacion.post("/tryon")
async def display_outfit(person: UploadFile, garment:list[UploadFile]):
    return await VisualizacionController.mostrarVisualizacionOutfit(person, garment)

@routerVisualizacion.post("/create")
async def create_visualizacion(usuarioId: PydanticObjectId, vestuarioId: list[PydanticObjectId], imagen_visualizacion: str):
    return await VisualizacionController.guardarVisualizacionOutfit(usuarioId, vestuarioId, imagen_visualizacion)