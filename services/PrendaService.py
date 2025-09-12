
from typing import Optional
from models.PrendaModel import Prenda
from schemas.PrendaSchema import Clothing
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from repository.PrendaRepository import PrendaRepository
from langchain_core.messages import HumanMessage, SystemMessage
from services.VisualizacionService import VisualizacionService
from beanie import PydanticObjectId
from PIL import Image
from pathlib import Path
import numpy as np
import base64
from io import BytesIO
from enums.PrendaCategoria import PrendaCategoria
from colorthief import ColorThief
from rembg import remove
import cv2

cloth_parser = PydanticOutputParser(pydantic_object=Clothing)
cloth_prompt = f"""
You are a visual assistant. Check if the provided image shows a clothing item.
If so, return the type of clothing item ONLY in English and whether it is for the upper or lower body.
Return EXACTLY one JSON object matching this schema:
{cloth_parser.get_format_instructions()}
""".strip()

class PrendaService:
     
    @staticmethod
    def codificar_imagen(path: Path) -> str:
        return base64.b64encode(path.read_bytes()).decode()
    
    @staticmethod
    async def classify_clothing(image_path: Path, llm: ChatOpenAI) -> Clothing:
        msgs = [
            SystemMessage(content=cloth_prompt),
            HumanMessage(content=[
                {"type": "text", "text": "Does the image show a clothing item?"},
                {"type": "image",
                "source_type": "base64",
                "data": VisualizacionService.codificar_imagen(image_path),
                "mime_type": "image/png"},
            ])
        ]
        structured = llm.with_structured_output(Clothing)
        for _ in range(3):
            res = structured.invoke(msgs)
            if res.hay_prenda and res.tipo_prenda and res.zona_cuerpo:
                return res
        return res

    @staticmethod
    def predict_model (model, image_base64:str) -> str:
        class_names = [e.value for e in PrendaCategoria]
        try: 
            image_bytes = base64.b64decode(image_base64)

            output = remove(image_bytes)
            img = Image.open(BytesIO(output)).convert("RGBA")

            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, img)

            img_gray = img.convert('L')

            img_array = np.array(img_gray).astype("float32") / 255.0
            img_array = cv2.resize(img_array, (28, 28))

            img_array = img_array.reshape(1, 28, 28, 1)

            probs = model.predict(img_array)[0]
            pred_class = int(np.argmax(probs))
            return class_names[pred_class]
        except Exception as e:
            raise RuntimeError(f"⚠️ Error en la predicción: {e}")
        
    @staticmethod
    def predict_model_lower (model, image_base64:str) -> str:
        class_names = [e.value for e in PrendaCategoria]
        try: 
            image_bytes = base64.b64decode(image_base64)

            output = remove(image_bytes)
            img = Image.open(BytesIO(output)).convert("RGBA")

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
            return class_names[pred_class]
        except Exception as e:
            raise RuntimeError(f"⚠️ Error en la predicción: {e}")

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
        except Exception as e:
            raise RuntimeError(f"No se pudo detectar el color predominante de la prenda: {e}")

    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await PrendaRepository.create_prenda(new_prenda)
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        try:
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return exist_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> list[Prenda]:
        try: 
            exist_prenda_usuario_id = await PrendaRepository.find_prenda_by_usuario_id(usuario_id)
            if not exist_prenda_usuario_id:
                raise Exception("No existen prendas asociadas a ese usuario ID")
            return exist_prenda_usuario_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> list[Prenda]:
        try:
            exist_prenda_tipo_prenda_id = await PrendaRepository.find_prenda_by_tipo_prenda_id(tipo_prenda_id)
            if not exist_prenda_tipo_prenda_id:
                raise Exception("No existen una prendas asociadas a ese tipo de prenda ID")
            return exist_prenda_tipo_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_name(name: str) -> list[Prenda]:
        try: 
            exist_prenda_name = await PrendaRepository.find_prenda_by_name(name)
            if not exist_prenda_name:
                raise Exception("No existe una prenda con ese nombre")
            return exist_prenda_name
        except Exception as error:
            raise error
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Optional[Prenda]:
        try: 
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return await PrendaRepository.delete_prenda(id)
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_prendas():
        try:
            prendas = await PrendaRepository.find_all_prendas()
            if not prendas:
                raise Exception("No existen prendas registradas")
            return prendas
        except Exception as error:
            raise error
    
    @staticmethod
    async def update_prenda(id: PydanticObjectId, update_prenda: dict) -> Prenda:
        try:
            exist_prenda = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda:
                raise Exception("No existe una prenda con ese ID")
            
            return await PrendaRepository.update_prenda(id, update_prenda)
        except Exception as error:
            raise error