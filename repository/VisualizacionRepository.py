from models.VisualizacionModel import Visualizacion

class VisualizacionRepository:

    @staticmethod
    async def create_visualizacion(visualizacion: Visualizacion) -> Visualizacion:
        return await Visualizacion.insert(visualizacion)