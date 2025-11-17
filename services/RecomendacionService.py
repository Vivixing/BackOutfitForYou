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
        lista_prendas = "\n".join(
            [RecomendacionService._prenda_a_str(p) for p in prendas])
        prompt = f"""
        Eres un experto en moda encargado de seleccionar prendas del usuario para crear una combinación de vestuario.

        A continuación tienes una lista de prendas en formato estructurado. 
        Cada ítem contiene:
        - id
        - nombre
        - color (hex)
        - categoría ("superior" o "inferior")
        - estilo
        - ocasiones (lista)

        PRNDAS DISPONIBLES:
        {lista_prendas}

        El usuario necesita una recomendación para la ocasión: "{ocasion}".

        =========================
        ### REGLAS OBLIGATORIAS
        Debes cumplir TODAS las siguientes reglas sin excepción:

        1. Selecciona EXACTAMENTE **dos prendas**.
        2. La primera prenda DEBE tener categoría **"superior"**.
        3. La segunda prenda DEBE tener categoría **"inferior"**.
        4. No puedes devolver dos superiores ni dos inferiores.
        5. Las prendas deben tener estilo compatible entre sí.
        6. Si existe una prenda con ocasión que coincida con "{ocasion}", debes priorizarla.
        7. Si no existe coincidencia exacta, selecciona la opción más compatible.
        8. Tu respuesta NO debe incluir explicaciones, texto adicional, descripciones ni comentarios.
        9. **SOLO** debes imprimir los IDs, uno por línea, en este orden:
        - Línea 1: id de la prenda superior
        - Línea 2: id de la prenda inferior

        =========================
        ### FORMATO DE RESPUESTA (OBLIGATORIO)

        <id_superior>
        <id_inferior>

        Sin guiones, sin comillas, sin palabras, sin nada más.

        Ahora genera la recomendación.
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
            raise Exception(
                "No es posible generar una recomendación porque el usuario no tiene prendas registradas.")

        # Validar cantidad mínima
        superiores = [
            p for p in prendas_usuario if p.tipoPrendaId.categoria.lower() == "superior"]
        inferiores = [
            p for p in prendas_usuario if p.tipoPrendaId.categoria.lower() == "inferior"]

        if len(superiores) < 2 or len(inferiores) < 2:
            raise Exception(
                "Debes tener al menos 2 prendas superiores y 2 prendas inferiores para generar una recomendación.")

        # Generar prompt y obtener IDs sugeridos
        prompt = await RecomendacionService.prompt(prendas_usuario, ocasion)
        respuesta = await RecomendacionService.obtener_recomendacion(prompt)

        ids_sugeridos = {line.strip("-•* ").strip()
                         for line in respuesta.splitlines() if line.strip()}

        # Filtro por prendas sugeridas
        prendas_sugeridas = [
            p for p in prendas_usuario if str(p.id) in ids_sugeridos]
        if not prendas_sugeridas:
            raise Exception(
                "Las prendas sugeridas no existen para este usuario")

        # ✅ VALIDACIÓN CRÍTICA: Verificar que haya 1 superior y 1 inferior
        superiores_sugeridas = [
            p for p in prendas_sugeridas if p.tipoPrendaId.categoria.lower() == "superior"]
        inferiores_sugeridas = [
            p for p in prendas_sugeridas if p.tipoPrendaId.categoria.lower() == "inferior"]

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

    async def guardar_recomendacion(usuarioId: PydanticObjectId, ocasion: str):

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
            vestuarioSugerido=vestuario.id,
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
                } for p in prendas_sugeridas_guardar
            ]
        }
