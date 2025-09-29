from typing import List
from models.RecomendacionModel import Recomendacion
from beanie import PydanticObjectId

class RecomendacionRepository:

    @staticmethod
    async def create_recomendacion(new_recomendacion: Recomendacion) -> Recomendacion:
        return await Recomendacion.insert(new_recomendacion)
    