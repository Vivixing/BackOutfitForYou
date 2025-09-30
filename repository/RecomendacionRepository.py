from models.RecomendacionModel import Recomendacion

class RecomendacionRepository:

    @staticmethod
    async def create_recomendacion(new_recomendacion: Recomendacion) -> Recomendacion:
        return await Recomendacion.insert(new_recomendacion)
    