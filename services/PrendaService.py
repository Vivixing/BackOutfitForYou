
from typing import Optional
from models.PrendaModel import Prenda
from schemas.PrendaSchema import Clothing, EtiquetaMetadata
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from repository.PrendaRepository import PrendaRepository
from langchain_core.messages import HumanMessage, SystemMessage
from beanie import PydanticObjectId
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from enums.PrendaCategoria import PrendaCategoria
from colorthief import ColorThief
import cv2

cloth_parser = PydanticOutputParser(pydantic_object=Clothing)
cloth_prompt = f"""
You are a visual assistant. Check if the provided image shows ONLY a clothing item.

If so, return the type of clothing item ONLY in English, specify whether it is for the upper or lower body, 
and confirm if the item is isolated (not worn by a person or mannequin).

Return EXACTLY one JSON object matching this schema:
{cloth_parser.get_format_instructions()}
""".strip()

etiqueta_parser = PydanticOutputParser(pydantic_object=EtiquetaMetadata)
etiqueta_prompt = """
Eres un asistente de moda. 
Analiza la prenda en la imagen y genera metadatos útiles para recomendaciones.

Devuelve un JSON con este formato
{etiqueta_parser.get_format_instructions()}
""".strip()


class PrendaService:
     
    @staticmethod
    def codificar_imagen(image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode()
    
    @staticmethod
    async def classify_clothing(image_bytes: bytes, llm: ChatOpenAI) -> Clothing:
        msgs = [
            SystemMessage(content=cloth_prompt),
            HumanMessage(content=[
                {"type": "text", "text": "Does the image show ONLY an isolated clothing item?"},
                {"type": "image", "source_type": "base64", "data": PrendaService.codificar_imagen(image_bytes), "mime_type": "image/png"},
            ])
        ]
        structured = llm.with_structured_output(Clothing)
        try:
            res = structured.invoke(msgs)
            if res.hay_prenda and res.tipo_prenda and res.zona_cuerpo and res.es_solo_prenda:
                return res
        except Exception:
            res = None
    
    @staticmethod
    async def etiquetar_prenda(image_bytes: bytes, llm: ChatOpenAI) -> dict:
        msgs = [
            SystemMessage(content=etiqueta_prompt),
            HumanMessage(content=[
                {"type": "text", "text": "Etiqueta esta prenda."},
                {"type": "image", "source_type": "base64", "data": PrendaService.codificar_imagen(image_bytes), "mime_type": "image/png"},
            ])
        ]
        structured = llm.with_structured_output(EtiquetaMetadata)
        try:
            res = structured.invoke(msgs)
            if res.estilo and res.ocasiones:  
                return res
        except Exception:
            return {"estilo": None, "ocasiones": []}

    @staticmethod
    def predict_model_white_bg(model, image_base64: str) -> str:
        """
        Predice la prenda reemplazando la transparencia por fondo blanco.
        """
        class_names = [e.value for e in PrendaCategoria]
        try:
            # Decodificar imagen
            image_bytes = base64.b64decode(image_base64)
            img = Image.open(BytesIO(image_bytes)).convert("RGBA")

            # Convertir a numpy
            img_rgba = np.array(img).astype("float32")

            # Separar canales
            rgb = img_rgba[:, :, :3]
            alpha = img_rgba[:, :, 3:4] / 255.0

            # Componer con fondo blanco
            img_rgb = rgb * alpha + 255 * (1 - alpha)

            # Convertir a grayscale si tu modelo lo necesita
            img_gray = cv2.cvtColor(img_rgb.astype("uint8"), cv2.COLOR_RGB2GRAY)

            # Redimensionar
            img_resized = cv2.resize(img_gray, (28, 28))

            # Ajustar shape para modelo
            img_input = img_resized.reshape(1, 28, 28, 1).astype("float32") / 255.0

            # Predicción
            probs = model.predict(img_input)[0]
            pred_class = int(np.argmax(probs))
            prediction = class_names[pred_class]

            if prediction.lower() in ["camiseta/top"]:
                prediction = "Camiseta"

            return prediction

        except Exception as e:
            raise RuntimeError(f"Ocurrió un problema al identificar la prenda. Detalle técnico: {e}")
        
    @staticmethod
    def predict_model_lower (model, image_base64:str) -> str:
        class_names = [e.value for e in PrendaCategoria]
        try: 
            image_bytes = base64.b64decode(image_base64)

            img = Image.open(BytesIO(image_bytes)).convert("RGBA")

            img_rgba = np.array(img)

            rgb = img_rgba[:, :, :3]
            alpha = img_rgba[:, :, 3]

            for c in range(3):
                rgb[:, :, c] = rgb[:, :, c] * (alpha / 255)

            img_gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

            img_array = img_gray.astype("float32") / 255.0
            img_array = cv2.resize(img_array, (28, 28))

            img_array = img_array.reshape(1, 28, 28, 1)

            probs = model.predict(img_array)[0]
            pred_class = int(np.argmax(probs))
            prediction = class_names[pred_class]

            if prediction.lower() in ["camiseta/top"]:
                prediction = "Camiseta"
            
            return prediction
        except Exception as e:
            raise RuntimeError(f"Ocurrió un problema al identificar la prenda. Inténtalo nuevamente. Detalle técnico: {e}")

    @staticmethod
    def obtener_color_predominante_prenda(image_base64:Image.Image) -> str:
        try:
            buffer = BytesIO()
            image_base64.save(buffer, format="PNG")
            buffer.seek(0)
            color_thief = ColorThief(buffer)
            color_rgb = color_thief.get_color(quality=1)
            color_hex = '#%02x%02x%02x' % color_rgb
            return color_hex.upper()
        except Exception:
            raise RuntimeError(f"No fue posible detectar el color principal de la prenda. Por favor, intenta con otra imagen.")

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        try:
            return await PrendaRepository.create_prenda(new_prenda)
        except Exception as e:
            raise Exception(e)    
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        try:
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No se encontró ninguna prenda con el identificador proporcionado.")
            return exist_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> list[Prenda]:
        try: 
            exist_prenda_usuario_id = await PrendaRepository.find_prenda_by_usuario_id(usuario_id)
            if not exist_prenda_usuario_id:
                raise Exception("Aún no tienes prendas registradas.")
            return exist_prenda_usuario_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> list[Prenda]:
        try:
            exist_prenda_tipo_prenda_id = await PrendaRepository.find_prenda_by_tipo_prenda_id(tipo_prenda_id)
            if not exist_prenda_tipo_prenda_id:
                raise Exception("No se encontraron prendas asociadas a ese tipo de categoría.")
            return exist_prenda_tipo_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Optional[Prenda]:
        try: 
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No se puede eliminar: la prenda indicada no existe.")
            return await PrendaRepository.delete_prenda(id)
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_prendas():
        try:
            prendas = await PrendaRepository.find_all_prendas()
            if not prendas:
                raise Exception("Aún no hay prendas registradas en la herramienta.")
            return prendas
        except Exception as error:
            raise error
    
    @staticmethod
    async def update_prenda(id: PydanticObjectId, update_prenda: dict) -> Prenda:
        try:
            exist_prenda = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda:
                raise Exception("No se pudo actualizar porque la prenda indicada no existe.")
            
            return await PrendaRepository.update_prenda(id, update_prenda)
        except Exception as error:
            raise error