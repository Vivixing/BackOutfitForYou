from schemas.RecomendacionSchema import RecomendacionRequest, RecomendacionResponse
from services.RecomendacionService import RecomendacionService
from models.RecomendacionModel import Recomendacion
from fastapi import HTTPException

class RecomendacionController:

    async def crear_recomendacion(data: RecomendacionRequest):
        try:
            recomendacion:Recomendacion = await RecomendacionService.generar_recomendacion(
                usuarioId = data.usuarioId,
                ocasion = data.ocasion
            )

            return RecomendacionResponse(
                id = str(recomendacion.id),
                usuarioId = str(recomendacion.usuarioId.id),
                ocasion = recomendacion.ocasion,
                vestuarioSugerido = [str(p.id) for p in recomendacion.vestuarioSugerido],
                fechaCreado = recomendacion.fechaCreado.isoformat()  
            )
        
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar recomendación: {str(e)}")