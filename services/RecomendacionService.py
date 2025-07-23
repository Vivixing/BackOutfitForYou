import datetime
from services.PrendaService import PrendaService
from repository.RecomendacionRepository import RecomendacionRepository
from core.openAI import client
from beanie import PydanticObjectId

class RecomendacionService:

    async def generar_recomendacion(usuarioId: str, ocasion: str):
        #Obtener prendas del usuario
        prendas = await PrendaService.find_prenda_by_usuario_id(usuarioId)

        # Separar superiores e inferiores
        prendas_superiores = [p for p in prendas if p.tipoPrenda.lower() == "Superior"]
        prendas_inferiores = [p for p in prendas if p.tipoPrenda.lower() == "Inferior"]
        
        # Crear prompt para OpenAI
        prompt = f"""Tú eres un asistente de moda. Un usuario describe la siguiente ocasión: "{ocasion}". 
        A continuación tienes una lista de prendas disponibles para ese usuario. Elige **una prenda superior y una inferior** considerando la ocasión y trata de combinar colores que armonicen visualmente para la ocasión descrita. 
        Solo responde con los nombres exactos de las prendas seleccionadas, separados por una coma.
 
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

        recomendacion_obj = recomendacion(
            usuarioId=PydanticObjectId(usuarioId),
            ocasion=ocasion,
            vestuarioSugerido=[PydanticObjectId(v_id) for v_id in vestuario_ids],
            fechaCreado=datetime.now()
        )

        # Guardar recomendación
        recomendacion = await RecomendacionRepository.crear_recomendacion(recomendacion_obj)
        return recomendacion