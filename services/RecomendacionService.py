import datetime
from services.PrendaService import PrendaService
from models.RecomendacionModel import Recomendacion
from repository.RecomendacionRepository import RecomendacionRepository
from core.openAI import client
from beanie import PydanticObjectId

class RecomendacionService:

    @staticmethod
    async def generar_recomendacion(usuarioId: PydanticObjectId, ocasion: str) -> list[str]:
        #Obtener prendas del usuario
        prendas = await PrendaService.find_prenda_by_usuario_id(usuarioId)

        # Separar superiores e inferiores
        prendas_superiores = [p for p in prendas if p.tipoPrenda.lower() == "Superior"]
        prendas_inferiores = [p for p in prendas if p.tipoPrenda.lower() == "Inferior"]
        
        # Crear prompt para OpenAI
        prompt = f"""Tú eres un asistente de moda. Un usuario describe la siguiente ocasión: "{ocasion}". 
        Estas son sus prendas disponibles. Elige **una prenda superior y una inferior** que combinen bien según la ocasión descrita.
        Combina colores de manera adecuada. Solo responde con los nombres exactos, separados por una coma.
 
        Prendas superiores:
        {chr(10).join([f"- {p.nombre} ({p.color})" for p in prendas_superiores])}
        
        Prendas inferiores:
        {chr(10).join([f"- {p.nombre} ({p.color})" for p in prendas_inferiores])}

        Respuesta esperada (formato): Prenda superior, Prenda inferior
        """

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de moda experto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        contenido = response.choices[0].message.content.strip()

        if "," in contenido:
            sup, inf = [s.strip() for s in contenido.split(",", 1)]
        else:
            raise ValueError("La respuesta no tiene el formato correcto.")
        
        # Buscar esas prendas en la base de datos
        prenda_sup = next((p for p in prendas_superiores if p.nombre == sup), None)
        prenda_inf = next((p for p in prendas_inferiores if p.nombre == inf), None)

        if not prenda_sup or not prenda_inf:
            raise ValueError("No se encontraron las prendas sugeridas.")
        
        vestuario_ids = [str(prenda_sup.id), str(prenda_inf.id)]
        return vestuario_ids

    @staticmethod
    async def guardar_recomendacion(usuarioId:PydanticObjectId, ocasion:str , vestuarios_ids:list[str]):
        recomendacion_obj = Recomendacion(
            usuarioId=PydanticObjectId(usuarioId),
            ocasion=ocasion,
            vestuarioSugerido=[PydanticObjectId(v_id) for v_id in vestuarios_ids],
            fechaCreado=datetime.now()
        )
        return await RecomendacionRepository.create_recomendacion(recomendacion_obj)