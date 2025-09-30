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

        Reglas estrictas:
        - Selecciona exactamente UNA prenda de categoría 'superior' y UNA de categoría 'inferior'.
        - Asegúrate de que ambas prendas sean coherentes con la ocasión solicitada y su estilo.
        - Prioriza prendas cuyo campo 'ocasiones' incluya la ocasión solicitada o sea compatible con ella.
        - Usa la información de estilo y color para asegurar armonía visual y coherencia.

        Si no existe ninguna combinación adecuada para la ocasión:
            • No inventes ni modifiques prendas.
            • En lugar de IDs, responde con la palabra clave **SIN_OPCION** en la primera línea.
            • En la segunda línea, escribe un breve mensaje proactivo sugiriendo al usuario qué tipo de prendas podría agregar para esa ocasión.
                Ejemplo:
                SIN_OPCION
                No se encontraron prendas adecuadas para la ocasión 'boda'. Se recomienda agregar prendas formales como un blazer, camisa o pantalón de vestir.
        
        - Usa todo EXACTO tal como aparece en la lista.

        En la respuesta final SOLO devolverás:
        - El ID de las prendas seleccionadas, cada uno en una línea separada, sin explicaciones
        - O el formato con SIN_OPCION + mensaje.

        Ejemplo de salida válida:
        688a7fd9225a99c1b7dfc86f
        688a8095225a99c1b7dfc870

        Ejemplo si no hay opciones:
        SIN_OPCION
        No encontramos prendas adecuadas para la ocasión. Te recomendamos agregar prendas formales como un blazer, camisa o pantalón de vestir.

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

        # Obtener prendas usuario
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

        # 🔍 Ver respuesta del modelo en consola
        print("==== RESPUESTA ORIGINAL DEL MODELO ====")
        print(repr(respuesta))  

        ids_sugeridos = [line.strip("-•* ").strip() for line in respuesta.splitlines() if line.strip()]
        
        if ids_sugeridos and ids_sugeridos[0] == "SIN_OPCION":
            mensaje_proactivo = "\n".join(ids_sugeridos[1:]) if len(ids_sugeridos) > 1 else "No fue posible generar una recomendación."
            raise Exception(mensaje_proactivo)

        # 🔍 Ver respuesta de los nombres sugueridos en consola
        print("==== LISTA DE IDS SUGERIDOS ====")
        print(ids_sugeridos)

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