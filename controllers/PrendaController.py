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
from io import BytesIO
import asyncio
from PIL import Image, ImageOps
import base64
import os
import datetime

# Inicialización global (al iniciar la app)
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))
model = load_h5_model()  # carga H5 solo una vez

class PrendaController:

    @staticmethod
    async def predict_prenda(imagen: UploadFile):
        loop = asyncio.get_event_loop()
        try:
            # Leer imagen en memoria
            image_bytes = await imagen.read()

            # Reducir tamaño de imagen antes de enviar al LLM
            img = Image.open(BytesIO(image_bytes))
            img = ImageOps.exif_transpose(img)
            img.thumbnail((512, 512))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            image_bytes_resized = buffered.getvalue()

            image_base64_llm = PrendaService.codificar_imagen(image_bytes_resized)

            # Clasificar prenda
            try:
                item = await PrendaService.classify_clothing(image_base64_llm, llm)
            except Exception:
                item = None

            # Validaciones iniciales
            if item is None or not item.hay_prenda:
                raise Exception("La imagen suministrada no parece ser una prenda de vestir.")
            
            if item is None or not item.es_solo_prenda:
                raise Exception("La imagen suministrada no es válida, por favor sube únicamente la prenda sin personas.")
            
            tagging_task = PrendaService.etiquetar_prenda(image_base64_llm, llm)
            remove_bg_task = loop.run_in_executor(None, remove, image_bytes_resized)

            results = await asyncio.gather(tagging_task, remove_bg_task, return_exceptions=True)

            tags = results[0]
            output_bytes = results[1]

            if isinstance(tags, Exception):
                print(f"Error en etiquetado: {tags}")
                tags = {"estilo": None, "ocasiones": []}
            if isinstance(output_bytes, Exception):
                raise output_bytes

            # --- Remover fondo UNA sola vez para todas las prendas ---
            img_transparent = Image.open(BytesIO(output_bytes)).convert("RGBA")

            color_task = loop.run_in_executor(None, PrendaService.obtener_color_predominante_prenda, img_transparent)

            nombre_prenda_predicho = "No detectada"
            mensaje_usuario = f"Tipo de prenda no permitido para predicción: {item.tipo_prenda}"
            prediction_task = None

            #Predicción solo si es un tipo permitido
            tipos_permitidos = ["jacket","pants","shirt","sweater","t-shirt","hoodie","jeans","pantalones","pantalón","camisa","camiseta","chaqueta","suéter","trouser","trousers"]
            if item.tipo_prenda.lower() in tipos_permitidos:
                # Predicción del modelo
                if item.zona_cuerpo.lower() == "superior":
                    prediction_task = loop.run_in_executor(None, PrendaService.predict_model_white_bg, model, img_transparent)
                else:
                    prediction_task = loop.run_in_executor(None, PrendaService.predict_model_lower, model, img_transparent)

            if prediction_task:
                pred_results = await asyncio.gather(color_task, prediction_task, return_exceptions=True)
                color = pred_results[0]
                pred_result = pred_results[1]

                if isinstance(pred_result, Exception):
                    nombre_prenda_predicho = nombre_prenda_predicho
                    mensaje_usuario = "Ocurrió un error al predecir la prenda."
                else: 
                    nombre_prenda_predicho = pred_result
                    mensaje_usuario = f"Prenda detectada: {nombre_prenda_predicho}"
            else:
                color = await color_task
            
            if isinstance(color, Exception):
                color = "No detectado"

            #Convertir a base64
            buffered_final = BytesIO()
            img_transparent.save(buffered_final, format="PNG")
            image_base64_transparent = base64.b64encode(buffered_final.getvalue()).decode()

            return {
                "status": 200,
                "nombre_prenda_predicha": nombre_prenda_predicho,
                "mensaje_usuario": mensaje_usuario,
                "color": color,
                "estilo": tags.get('estilo') if isinstance(tags, dict) else tags.estilo,
                "ocasiones": tags.get('ocasiones') if isinstance(tags, dict) else tags.ocasiones,
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
                estilo=request.estilo,
                ocasiones=request.ocasiones,
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