from beanie import PydanticObjectId
from schemas.RecomendacionSchema import RecomendacionRequest, RecomendacionResponse
from services.RecomendacionService import RecomendacionService
from fastapi import HTTPException

class RecomendacionController:

    @staticmethod
    async def generar_recomendacion(usuarioId:PydanticObjectId, ocasion:str) -> list[str]:
        try:
            return await RecomendacionService.generar_recomendacion(usuarioId, ocasion)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar recomendación: {str(e)}")
        
    @staticmethod
    async def guardar_recomendacion(usuarioId:PydanticObjectId, ocasion:str, vestuarios_ids:list[str]) -> RecomendacionResponse:
        try:
            recomendacion = await RecomendacionService.guardar_recomendacion(usuarioId, ocasion, vestuarios_ids)
            return RecomendacionResponse(
                id=str(recomendacion.id),
                usuarioId=str(recomendacion.usuarioId.id),
                ocasion=recomendacion.ocasion,
                vestuarioSugerido=[str(p.id) for p in recomendacion.vestuarioSugerido],
                fechaCreado=recomendacion.fechaCreado.isoformat()
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar recomendación: {str(e)}")