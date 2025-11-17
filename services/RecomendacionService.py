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

        ⚠️ INSTRUCCIONES CRÍTICAS - DEBES CUMPLIRLAS AL 100%:
        1. Debes seleccionar **EXACTAMENTE DOS PRENDAS en total**.  
        2. La PRIMERA línea DEBE ser el ID de una prenda con categoría **"superior"**.  
        3. La SEGUNDA línea DEBE ser el ID de una prenda con categoría **"inferior"**.  
        4. NUNCA devuelvas dos prendas de la misma categoría (ni dos superiores, ni dos inferiores).
        5. Revisa bien el campo "categoría" de cada prenda antes de seleccionarla.
        6. Prioriza prendas cuyo campo 'ocasiones' incluya la ocasión solicitada o sea compatible.  
        7. Asegúrate de que ambas prendas sean coherentes en estilo y color.  
        8. SOLO devuelve los IDs, sin texto adicional, sin explicaciones, sin guiones, sin numeración.

        📌 FORMATO DE RESPUESTA (OBLIGATORIO):
        Línea 1: ID de UNA prenda superior
        Línea 2: ID de UNA prenda inferior

        Ejemplo correcto:
        688a7fd9225a99c1b7dfc86f
        688a8095225a99c1b7dfc870

        Ahora proporciona tu recomendación (solo dos IDs, uno por línea):
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
        
        # ✅ VALIDACIÓN CRÍTICA: Verificar que haya 1 superior y 1 inferior
        superiores_sugeridas = [p for p in prendas_sugeridas if p.tipoPrendaId.categoria.lower() == "superior"]
        inferiores_sugeridas = [p for p in prendas_sugeridas if p.tipoPrendaId.categoria.lower() == "inferior"]

        # Si la IA falló, corregir manualmente
        if len(superiores_sugeridas) != 1 or len(inferiores_sugeridas) != 1:
            # Tomar la primera/mejor superior e inferior disponibles que coincidan con la ocasión
            prenda_superior = None
            prenda_inferior = None
            
            # Buscar prendas que mencionen la ocasión
            for p in superiores:
                if ocasion.lower() in [oc.lower() for oc in p.ocasiones]:
                    prenda_superior = p
                    break
            if not prenda_superior:
                prenda_superior = superiores[0]  # Fallback: primera disponible
            
            for p in inferiores:
                if ocasion.lower() in [oc.lower() for oc in p.ocasiones]:
                    prenda_inferior = p
                    break
            if not prenda_inferior:
                prenda_inferior = inferiores[0]  # Fallback: primera disponible
            
            prendas_sugeridas = [prenda_superior, prenda_inferior]

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