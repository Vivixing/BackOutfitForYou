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
        Estas son las prendas disponibles del usuario:
        {lista_prendas}
        El usuario desea una recomendación de vestiario para la siguiente ocasión: "{ocasion}".
        Elige **una prenda superior y una inferior** que combinen bien según la ocasión descrita.
        Devuélveme solo los nombres exactos de las prendas seleccionadas.
        """
        return prompt
    
    @staticmethod 
    async def obtener_recomendacion(prompt: str):
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        contenido = response.choices[0].message.content.strip()
        return contenido
    
    @staticmethod
    async def obtener_prendas_usuario(usuarioId: PydanticObjectId, nombres:list[str]):  
        # Obtener prendas del usuario
        prendas = await PrendaService.find_prenda_by_usuario_id(usuarioId)

        # Filtrar prendas por nombres
        prendas_filtradas = [p for p in prendas if p.nombre in nombres]

        if not prendas_filtradas:
            raise ValueError("No se encontraron prendas con los nombres proporcionados.")
        
        return prendas_filtradas
    

    @staticmethod
    async def generar_recomendacion(usuarioId: PydanticObjectId, ocasion: str):
       
       prendas_usuario = await PrendaService.find_prenda_by_usuario_id(usuarioId)
       prendas_activas = [p for p in prendas_usuario if p.estado == "true"]

       prompt = await RecomendacionService.prompt(prendas_activas, ocasion)

       respuesta = await RecomendacionService.obtener_recomendacion(prompt)
       nombres_sugeridos = [line.strip("-•* ").strip() for line in respuesta.splitlines() if line.strip()]

       prendas_sugeridas = await RecomendacionService.obtener_prendas_usuario(usuarioId, nombres_sugeridos)

       vestuario = Vestuario(
           usuarioId=usuarioId,
           prendas=[p.id for p in prendas_sugeridas],
           ocasion=ocasion,
           fechaCreacion=datetime.datetime.now()
        )

       await VestuarioRepository.create_vestuario(vestuario)

       recomendacion = Recomendacion(
           usuarioId=usuarioId,
           ocasion=ocasion,
           vestuarioSugerido=[p.id for p in prendas_sugeridas],
           fechaCreado=datetime.datetime.now()
        )

       await RecomendacionRepository.create_recomendacion(recomendacion)

       resultado = {
           "ocasion": ocasion,
           "vestuarioSugerido": [
               {
                   "nombre": p.nombre,
                   "color": p.color,
                   "categoria": p.tipoPrendaId.categoria,
                   "imagen": p.imagen,
               } for p in prendas_sugeridas
           ]
       }

       return resultado