import datetime
from beanie import PydanticObjectId
from core.modelLoader import load_h5_model
from models.PrendaModel import Prenda
from services.UsuarioService import UsuarioService
from services.TipoPrendaService import TipoPrendaService
from schemas.PrendaSchema import PrendaCreadoRequest, PrendaActualizadoRequest
from services.PrendaService import PrendaService
from fastapi import HTTPException, UploadFile
import base64

class PrendaController:

    @staticmethod
    async def predict_prenda(imagen: UploadFile):
        try:
            #Cargar el modelo una sola vez
            model = load_h5_model()
            #convertir imagen a bytes
            imagen_bytes = await imagen.read()
            imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

            #Predicción de la prenda con modelo
            try:
                nombrePrenda_predicho = PrendaService.predict_model(model, imagen_base64)
            except Exception:
                nombrePrenda_predicho = None
 
            #Detectar color
            try:
                color = PrendaService.obtener_color_predominante_prenda(imagen_base64)
            except Exception:
                color = None

            return {
            "status": 200,
            "nombre_prenda_predicha": nombrePrenda_predicho if nombrePrenda_predicho else "No detectada",
            "color": color if color else "No detectado",
            "imagen_base64": imagen_base64  # Para que el cliente pueda enviarla en /create si quiere
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    @staticmethod
    async def create_prenda(request:PrendaCreadoRequest):
        try:
            usuario = await UsuarioService.find_user_by_id(PydanticObjectId(request.usuarioId))
            tipo_prenda = await TipoPrendaService.find_tipo_prenda_by_id(PydanticObjectId(request.tipoPrendaId)) 

            prenda_convert = Prenda(
                usuarioId=usuario,
                tipoPrendaId=tipo_prenda,
                nombre=request.nombre,
                color=request.color,
                imagen=request.imagen_base64,
                fechaCreado=datetime.datetime.now(),
                fechaModificado=datetime.datetime.now(),
                estado=True
            )

            prenda = await PrendaService.create_prenda(prenda_convert)

            return {"status": 200, "message": "Prenda creada correctamente", "id_Prenda": prenda.id, "nombre_predicho": prenda.nombre, "color_detectado":prenda.color, "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    
    @staticmethod
    async def get_prenda_by_id(prenda_id:PydanticObjectId):
        try:
            prenda = await PrendaService.find_prenda_by_id(prenda_id)
            return {"status": 200, "message": "Prenda encontrada", "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prendas_by_user(user_id:PydanticObjectId):
        try:
            prendas = await PrendaService.find_prenda_by_usuario_id(user_id)
            return {"status": 200, "message": "Prendas encontradas", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prendas_by_tipo_prenda(tipo_prenda_id:PydanticObjectId):
        try:
            prendas = await PrendaService.find_prenda_by_tipo_prenda_id(tipo_prenda_id)
            return {"status": 200, "message": "Prendas encontradas", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_prenda_by_name(name:str):
        try:
            prenda = await PrendaService.find_prenda_by_name(name)
            return {"status": 200, "message": "Prenda encontrada", "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def get_all_prendas():
        try:
            prendas = await PrendaService.find_all_prendas()
            return {"status": 200, "message": f"Prendas encontradas {len(prendas)}", "data": prendas}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @staticmethod
    async def update_prenda(id:PydanticObjectId, request:PrendaActualizadoRequest):
        try:
            update_data = request.dict(exclude_unset=True)

            if not update_data:
                raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
             
            prenda = await PrendaService.update_prenda(id, update_data)
            return {"status": 200, "message": "Prenda actualizada correctamente", "prenda_id":str(prenda.id), "data": prenda}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    async def delete_prenda(prenda_id:PydanticObjectId):
        try:
            prenda = await PrendaService.delete_prenda(prenda_id)
            return {"status": 200, "message": "Prenda marcada como inactiva","data": prenda}
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=404, detail=str(e))