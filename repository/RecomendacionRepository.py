from models.RecomendacionModel import Recomendacion
from beanie import PydanticObjectId

class RecomendacionRepository:

    @staticmethod
    async def create_recomendacion(new_recomendacion: Recomendacion) -> Recomendacion:
        return await Recomendacion.insert(new_recomendacion)
    
    @staticmethod
    async def find_recomendaciones_by_usuario_id(usuario_id:  PydanticObjectId)-> list[Recomendacion]:
        return await Recomendacion.find(Recomendacion.usuarioId.id == usuario_id).to_list()