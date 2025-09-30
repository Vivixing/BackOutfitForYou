from repository.RecomendacionRepository import RecomendacionRepository
from services.VestuarioService import VestuarioService
from models.RecomendacionModel import Recomendacion
from services.PrendaService import PrendaService
from models.VestuarioModel import Vestuario
from core.openAI import openai_client
from beanie import PydanticObjectId
import datetime

class RecomendacionService:

    @staticmethod
    def _prenda_a_str(p) -> str:
        return f"- ID_Prenda: {p.id}, nombre {p.nombre}, color {p.color}, categoría {p.tipoPrendaId.categoria}, estilo prenda {p.estilo} y ocasiones {p.ocasiones}"

    @staticmethod
    async def prompt(prendas: list[str], ocasion: str) -> str:
        lista_prendas = "\n".join([RecomendacionService._prenda_a_str(p) for p in prendas])
        prompt = f"""Eres un asesor de moda experto en combinar prendas según su estilo, ocasión de uso y armonía de colores.
        
        Tienes la siguiente lista de prendas del usuario. 
        Cada prenda incluye su nombre, el color en código hexadecimal, su categoría (superior o inferior), estilo general (casual, formal, elegante, etc.).
        y ocasiones sugeridas (boda, oficina, deporte, diario, etc.) 
        
        Lista de prendas disponibles:
        {lista_prendas}
        
        El usuario desea una recomendación de vestuario para la siguiente ocasión: "{ocasion}".

        ⚠️ INSTRUCCIONES ESTRICTAS (OBLIGATORIAS):
        1. Debes seleccionar **exactamente dos prendas en total**.  
        2. Una prenda DEBE ser de la categoría **superior**.  
        3. La otra prenda DEBE ser de la categoría **inferior**.  
        4. No está permitido devolver dos prendas de la misma categoría.  
        5. Prioriza prendas cuyo campo 'ocasiones' incluya la ocasión solicitada o sea compatible con ella.  
        6. Asegúrate de que ambas prendas sean coherentes en estilo y color.  
        7. No inventes, no expliques, no agregues texto adicional. 

        📌 FORMATO DE RESPUESTA (obligatorio):
        Solo devuelve **dos líneas**, cada una con un ID de prenda.  
        Primera línea: ID de la prenda superior.  
        Segunda línea: ID de la prenda inferior.

        Ejemplo de salida válida:
        688a7fd9225a99c1b7dfc86f
        688a8095225a99c1b7dfc870

        Ahora proporciona tu recomendación:
        """
        return prompt
    
    @staticmethod 
    async def obtener_recomendacion(prompt: str):
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=50
        )
        contenido = response.choices[0].message.content.strip()
        return contenido    

    @staticmethod
    async def generar_recomendacion(usuarioId: PydanticObjectId, ocasion: str):

        try:
            prendas_usuario = await PrendaService.find_prenda_by_usuario_id(usuarioId)
        except Exception:
            raise Exception("No es posible generar una recomendación porque el usuario no tiene prendas registradas.")
        
        # Validar cantidad mínima
        superiores = [p for p in prendas_usuario if p.tipoPrendaId.categoria.lower() == "superior"]
        inferiores = [p for p in prendas_usuario if p.tipoPrendaId.categoria.lower() == "inferior"]

        if len(superiores) < 2 or len(inferiores) < 2:
            raise Exception("Debes tener al menos 2 prendas superiores y 2 prendas inferiores para generar una recomendación.")

        #Generar prompt y obtener IDs sugeridos
        prompt = await RecomendacionService.prompt(prendas_usuario, ocasion)
        respuesta = await RecomendacionService.obtener_recomendacion(prompt)

        ids_sugeridos = {line.strip("-•* ").strip() for line in respuesta.splitlines() if line.strip()}

        #Filtro por prendas sugeridas
        prendas_sugeridas = [p for p in prendas_usuario if str(p.id) in ids_sugeridos]
        if not prendas_sugeridas:
            raise Exception("Las prendas sugeridas no existen para este usuario")   

        return prendas_sugeridas
    
    async def guardar_recomendacion(usuarioId:PydanticObjectId, ocasion: str):
        
        prendas_sugeridas_guardar = await RecomendacionService.generar_recomendacion(usuarioId, ocasion)

        vestuario = Vestuario(
            usuarioId=usuarioId,
            prendas=[p.id for p in prendas_sugeridas_guardar],
            fechaCreacion=datetime.datetime.now()
        )
        await VestuarioService.create_vestuario(vestuario)

        recomendacion = Recomendacion(
            usuarioId=usuarioId,
            ocasion=ocasion,
            vestuarioSugerido= vestuario.id,
            fechaCreado=datetime.datetime.now()
        )
        await RecomendacionRepository.create_recomendacion(recomendacion)

        return {
            "ocasion": ocasion,
            "vestuarioId": str(vestuario.id),
            "vestuario Sugerido": [
                {
                    "id": str(p.id),
                    "nombre": p.nombre,
                    "color:": p.color,
                    "categoría": p.tipoPrendaId.categoria,
                    "imagen": p.imagen,
                } for p in  prendas_sugeridas_guardar
            ]
        }