from beanie import PydanticObjectId
from fastapi import UploadFile, HTTPException
from services.VisualizacionService import VisualizacionService
import base64
import tempfile
import os

class VisualizacionController:

    @staticmethod
    async def mostrarVisualizacionOutfit(person: UploadFile, garment:list[UploadFile]):
        
        # Guardar temporalmente los archivos subidos
        temp_dir = tempfile.gettempdir()
        person_path = os.path.join(temp_dir, f"person_{person.filename}")
        clothing_paths = [os.path.join(temp_dir, f"clothing_{c.filename}") for c in garment]

        try:

            with open(person_path, "wb") as f:
                f.write(await person.read())
            
            for i, c in enumerate(garment):
                with open(clothing_paths[i], "wb") as f:
                    f.write(await c.read())

            result, error = await VisualizacionService.try_on(person_path, clothing_paths)
            if error:
                raise HTTPException(status_code=400, detail=error)
            
            with open(result, "rb") as f:
                img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

            return {"image_base64": img_base64}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    async def guardarVisualizacionOutfit(usuarioId: str, vestuarioId: str, imagen_visualizacion: str):
        try:
            visualizacion = await VisualizacionService.createVisualizacion(usuarioId, vestuarioId, imagen_visualizacion)
            return {"message": "Visualización guardada exitosamente", "data": visualizacion}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def obtenerVisualizacionesPorUsuario(usuarioId: PydanticObjectId):
        try:
            visualizaciones = await VisualizacionService.getVisualizacionesByUserId(usuarioId)
            return {"data": visualizaciones}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))