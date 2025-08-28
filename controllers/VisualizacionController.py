from fastapi import UploadFile, HTTPException
from services.VisualizacionService import VisualizacionService
from fastapi.responses import FileResponse
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
            
            return FileResponse(result, media_type="image/png", filename="outfit.png")
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
