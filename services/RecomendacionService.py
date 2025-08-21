import datetime
from models.VestuarioModel import Vestuario
from repository.VestuarioRepository import VestuarioRepository
from services.PrendaService import PrendaService
from models.RecomendacionModel import Recomendacion
from repository.RecomendacionRepository import RecomendacionRepository
from core.openAI import openai_client
from beanie import PydanticObjectId

class RecomendacionService:

    @staticmethod
    async def prompt(prendas: list[str], ocasion: str) -> str:
        lista_prendas = "\n".join([
            f"- {p.nombre}, color {p.color}, categoría {p.tipoPrendaId.categoria}"
            for p in prendas
        ])
        prompt = f"""Eres un asistente de moda.
        Tienes la siguiente lista de prendas del usuario. 
        Cada prenda incluye su nombre, el color en código hexadecimal y su categoría (superior o inferior).
        Debes considerar todos estos atributos para hacer tu recomendación, pero en la respuesta final SOLO devolverás el nombre exacto de las prendas seleccionadas.
        
        Lista de prendas disponibles:
        {lista_prendas}
        
        El usuario desea una recomendación de vestuario para la siguiente ocasión: "{ocasion}".

        Reglas estrictas:
        - Elige exactamente UNA prenda de categoría 'superior' y UNA de categoría 'inferior' que combinen bien con la ocasión.
        - NO inventes prendas, colores ni categorías.
        - Usa los nombres EXACTOS tal como aparecen en la lista.
        - No cambies el orden ni la ortografía de los nombres.
        - La respuesta final debe contener únicamente los nombres exactos de las prendas, cada uno en una línea separada, sin comentarios, colores ni categorías.

        Ejemplo de salida válida:
        Camisa
        Pantalón

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
        )
        contenido = response.choices[0].message.content.strip()
        return contenido
    
    @staticmethod
    async def obtener_prendas_usuario(usuarioId: PydanticObjectId, nombres_sugeridos: list[str]):  
        
        prendas = await PrendaService.find_prenda_by_usuario_id(usuarioId)

        # Filtrar prendas por nombres
        prendas_filtradas = [
            p for p in prendas if p.nombre in nombres_sugeridos]

        if not prendas_filtradas:
            raise ValueError("No se encontraron prendas con los nombres proporcionados.")
        
        return prendas_filtradas
    

    @staticmethod
    async def generar_recomendacion(usuarioId: PydanticObjectId, ocasion: str):
       
       # Solo genera la recomendación 
        prendas_usuario = await PrendaService.find_prenda_by_usuario_id(usuarioId)
        prendas_activas = [p for p in prendas_usuario if p.estado]
       
        # 🔍 Ver prendas activas en consola
        print("\n=== PRENDAS ACTIVAS DEL USUARIO ===")
        for p in prendas_activas:
            print(f"- {p.nombre}, color {p.color}, categoría {p.tipoPrendaId.categoria}")
        print("===================================\n")

        prompt = await RecomendacionService.prompt(prendas_activas, ocasion)
        respuesta = await RecomendacionService.obtener_recomendacion(prompt)

        # 🔍 Ver respuesta del modelo en consola
        print("==== RESPUESTA ORIGINAL DEL MODELO ====")
        print(repr(respuesta))  

        nombres_sugeridos = [line.strip("-•* ").strip() for line in respuesta.splitlines() if line.strip()]

        # 🔍 Ver respuesta de los nombres sugueridos en consola
        print("==== LISTA DE NOMBRES SUGERIDOS ====")
        print(nombres_sugeridos)

        prendas_sugeridas = await RecomendacionService.obtener_prendas_usuario(usuarioId, nombres_sugeridos)   

        return prendas_sugeridas
    
    async def guardar_recomendacion(usuarioId:PydanticObjectId, ocasion: str):
        
        prendas_sugeridas_guardar = await RecomendacionService.generar_recomendacion(usuarioId, ocasion)

        vestuario = Vestuario(
            usuarioId=usuarioId,
            prendas=[p.id for p in prendas_sugeridas_guardar],
            fechaCreacion=datetime.datetime.now()
        )
        await VestuarioRepository.create_vestuario(vestuario)

        recomendacion = Recomendacion(
            usuarioId=usuarioId,
            ocasion=ocasion,
            vestuarioSugerido=[p.id for p in prendas_sugeridas_guardar],
            fechaCreado=datetime.datetime.now()
        )
        await RecomendacionRepository.create_recomendacion(recomendacion)

        return {
            "ocasion": ocasion,
            "vestuario Sugerido": [
                {
                    "nombre": p.nombre,
                    "color:": p.color,
                    "categoría": p.tipoPrendaId.categoria,
                    "imagen": p.imagen,
                } for p in  prendas_sugeridas_guardar
            ]
        }