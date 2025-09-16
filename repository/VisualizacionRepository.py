from beanie import PydanticObjectId
from models.VisualizacionModel import Visualizacion

class VisualizacionRepository:

    @staticmethod
    async def create_visualizacion(visualizacion: Visualizacion) -> Visualizacion:
        return await Visualizacion.insert(visualizacion)
    
    @staticmethod
    async def get_visualizacion_by_user_id(usuarioId: PydanticObjectId) -> list[Visualizacion]:
        return await Visualizacion.find(Visualizacion.usuarioId.id == usuarioId).to_list()