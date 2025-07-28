from beanie import PydanticObjectId
from services.RecomendacionService import RecomendacionService
from fastapi import HTTPException

class RecomendacionController:

    @staticmethod
    async def generar_recomendacion(usuarioId: PydanticObjectId, ocasion: str):
        try:
            recomendacion = await RecomendacionService.generar_recomendacion(usuarioId, ocasion)
            return {"message": "Recomendación generada exitosamente", "data": recomendacion}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))