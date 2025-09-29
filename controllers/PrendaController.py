from beanie import PydanticObjectId
from models.PrendaModel import Prenda
from services.UsuarioService import UsuarioService
from services.TipoPrendaService import TipoPrendaService
from schemas.PrendaSchema import PrendaCreadoRequest, PrendaActualizadoRequest
from services.PrendaService import PrendaService
from fastapi import HTTPException, UploadFile
from core.modelLoader import load_h5_model
from langchain_openai import ChatOpenAI
from rembg import remove
from pathlib import Path
from io import BytesIO
from PIL import Image
import base64
import os
import tempfile
import time
import datetime

# Inicialización global (al iniciar la app)
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))
model = load_h5_model()  # carga H5 solo una vez

class PrendaController:

    @staticmethod
    async def predict_prenda(imagen: UploadFile):

        start_total = time.time()

        temp_dir = tempfile.gettempdir()
        clothing_path = os.path.join(temp_dir, f"clothing_{imagen.filename}")

        try:
            # Guardar archivo temporalmente
            with open(clothing_path, "wb") as f:
                f.write(await imagen.read())

            # Reducir tamaño de imagen antes de enviar al LLM
            img = Image.open(clothing_path)
            img.thumbnail((512, 512))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Clasificar prenda
            try:
                t1 = time.time()
                item = await PrendaService.classify_clothing(Path(clothing_path), llm)
                print("Clasificación LLM:", time.time() - t1, "segundos")
            except Exception:
                item = None

            # Validaciones iniciales
            if item is None or not item.hay_prenda:
                raise Exception("La imagen suministrada no parece ser una prenda de vestir.")
            
            if item is None or not item.es_solo_prenda:
                raise Exception("La imagen suministrada no es válida, por favor sube únicamente la prenda sin personas.")
            
            # --- Remover fondo UNA sola vez para todas las prendas ---
            t2 = time.time()
            input_bytes = open(clothing_path, "rb").read()
            output_bytes = remove(input_bytes)
            img_transparent = Image.open(BytesIO(output_bytes)).convert("RGBA")
            print("Remoción de fondo:", time.time() - t2, "segundos")

            # Codificar la imagen removida en base64 para la predicción
            buffered = BytesIO()
            img_transparent.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()

            #Predicción solo si es un tipo permitido
            tipos_permitidos = ["jacket","pants","shirt","sweater","t-shirt","hoodie"]
            if item.tipo_prenda.lower() not in tipos_permitidos:
                nombre_prenda_predicho = "No detectada"
                mensaje_usuario = f"Tipo de prenda no permitido para predicción: {item.tipo_prenda}"
            else:
                try:
                    # Predicción del modelo
                    t3 = time.time()
                    
                    if item.zona_cuerpo.lower() == "superior":
                        nombre_prenda_predicho = PrendaService.predict_model(model, image_base64)
                    else:
                        nombre_prenda_predicho = PrendaService.predict_model_lower(model, image_base64)
                    print("Predicción modelo:", time.time() - t3, "segundos")
                    mensaje_usuario = f"Prenda detectada: {nombre_prenda_predicho}"
                except Exception:
                    nombre_prenda_predicho = "No detectada"
                    mensaje_usuario = "Ocurrió un error al predecir la prenda."

            # Detectar color siempre que sea prenda
            try:
                t4 = time.time()
                color = PrendaService.obtener_color_predominante_prenda(img_transparent)
                print("Detección de color:", time.time() - t4, "segundos")
            except Exception:
                color = "No detectado"

            #Convertir a base64
            buffered_final = BytesIO()
            img_transparent.save(buffered_final, format="PNG")
            image_base64_transparent = base64.b64encode(buffered_final.getvalue()).decode()

            print("Tiempo total predict_prenda:", time.time() - start_total, "segundos")

            return {
                "status": 200,
                "nombre_prenda_predicha": nombre_prenda_predicho,
                "mensaje_usuario": mensaje_usuario,
                "color": color,
                "imagen_base64": image_base64_transparent
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_prenda(request:PrendaCreadoRequest):
        try:
            usuario = await UsuarioService.find_user_by_id(request.usuarioId)
            tipo_prenda = await TipoPrendaService.find_tipo_prenda_by_id(request.tipoPrendaId) 

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