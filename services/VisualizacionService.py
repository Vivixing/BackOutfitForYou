from beanie import PydanticObjectId
from repository.VisualizacionRepository import VisualizacionRepository
from schemas.VisualizacionSchema import ClothingItem, Person
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from models.VisualizacionModel import Visualizacion
from repository.VestuarioRepository import VestuarioRepository
from repository.UsuarioRepository import UsuarioRepository
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pathlib import Path
from typing import List
import tempfile
import datetime
import base64
import uuid
import os

person_parser = PydanticOutputParser(pydantic_object=Person)
person_prompt = f"""
You are a vision assistant. Check if the provided image shows a person.
If so, describe the person in the image in one sentence.
Return EXACTLY one JSON object matching this schema:
{person_parser.get_format_instructions()}
""".strip()

cloth_parser = PydanticOutputParser(pydantic_object=ClothingItem)
cloth_prompt = f"""
You are a visual assistant. Check if the provided image shows clothing item.
If so, return type of the clothing item.
Return EXACTLY one JSON object matching this schema:
{cloth_parser.get_format_instructions()}
""".strip()

class VisualizacionService:

    @staticmethod
    def codificar_imagen(path: Path) -> str:
        return base64.b64encode(path.read_bytes()).decode()
    
    @staticmethod
    async def classify_person(image_path: Path, llm: ChatOpenAI) -> Person:
        msgs = [
            SystemMessage(content=person_prompt),
            HumanMessage(content=[
                {"type": "text", "text": "Does the image show a person?"},
                {"type": "image",
                "source_type": "base64",
                "data": VisualizacionService.codificar_imagen(image_path),
                "mime_type": "image/png"},
            ])
        ]
        structured = llm.with_structured_output(Person)
        for _ in range(3):
            res = structured.invoke(msgs)
            if res.hay_persona and res.descripcion:
                return res
        return res

    @staticmethod
    async def classify_clothing(image_path: Path, llm: ChatOpenAI) -> ClothingItem:
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
        structured = llm.with_structured_output(ClothingItem)
        for _ in range(3):
            res = structured.invoke(msgs)
            if res.hay_prendas and res.tipo_prenda:
                return res
        return res

    @staticmethod
    async def try_on(person_fp: str, clothing_fps: list[str]):

        if len(clothing_fps) > 2:
            return None, "Solo puede cargar hasta 2 prendas a la vez."

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None, "No se encontró la clave de acceso al servicio."

        llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key, max_tokens=200)
        img_client = OpenAI(api_key=api_key)

        person = await VisualizacionService.classify_person(Path(person_fp), llm)
        if not person.hay_persona:
            return None, "La imagen debe contener claramente a una persona."

        clothing_results, invalid = [], []
        for fp in clothing_fps:
            item = await VisualizacionService.classify_clothing(Path(fp), llm)
            if item.hay_prendas:
                clothing_results.append(item)
            else:
                invalid.append(Path(fp).name)
        if invalid:
            return None, f"Los siguientes archivos no parecen ser prendas de vestir: {', '.join(invalid)}"
        
        types = [c.tipo_prenda for c in clothing_results]
        prompt_text = (
            f"Generate a photorealistic image of the {person.descripcion}"
            f"wearing the provided {' and '.join(types)} on a clean white background."
        )
        try:
            files = [open(person_fp, "rb")] + [open(fp, "rb") for fp in clothing_fps]

            resp = img_client.images.edit( 
                model="gpt-image-1",
                image= files,
                prompt=prompt_text,
                quality= "low",
                size="1024x1024",
                n=1
            )

            for f in files:
                f.close()

            out_path = Path(tempfile.gettempdir()) / f"composite_{uuid.uuid4().hex}.png"
            out_path.write_bytes(base64.b64decode(resp.data[0].b64_json))
            return str(out_path), ""
        except Exception:
            return None, f"Hubo un problema al generar la visualización. Inténtelo nuevamente más tarde."
        
    @staticmethod
    async def createVisualizacion(usuarioId: str, vestuarioId: str, imagen_visualizacion: str):

        try:
            if not usuarioId:
                raise Exception("El usuario es obligatorio.")
            exist_usuario_by_id = await UsuarioRepository.find_user_by_id(usuarioId)
            if not exist_usuario_by_id:
                raise Exception("El usuario no existe.")
            
            if not vestuarioId:
                raise Exception("El vestuario es obligatorio.")
            
            if not imagen_visualizacion:
                raise Exception ("La imagen de la visualización es obligatoria.")
            if not imagen_visualizacion.startswith("data:image/") and not imagen_visualizacion.strip():
                raise Exception("El formato de la imagen no es válido.")
        
            visualizacion = Visualizacion(
                usuarioId=usuarioId,
                vestuarioId=vestuarioId,
                imagen=imagen_visualizacion,
                fechaCreado= datetime.datetime.now()
            )
            return await VisualizacionRepository.create_visualizacion(visualizacion)
        except Exception as error:
            raise error
    
    @staticmethod
    async def getVisualizacionesByUserId(usuarioId: PydanticObjectId) -> List[Visualizacion]:
        try: 
            exist_visualizaciones_by_usuario = await VisualizacionRepository.get_visualizacion_by_user_id(usuarioId)
            if not exist_visualizaciones_by_usuario:
                raise Exception("Aún no tienes visualizaciones registradas.")
            return exist_visualizaciones_by_usuario
        except Exception as error:
            raise error