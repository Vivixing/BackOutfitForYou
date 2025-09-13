from controllers.VestuarioController import VestuarioController
from beanie import PydanticObjectId
from fastapi import APIRouter

routerVestuario = APIRouter(prefix="/wardrobe", tags=["Vestuario"])

@routerVestuario.get("/{vestuarioId}", response_model=dict)
async def get_vestuario_by_id(vestuarioId: PydanticObjectId):
    return await VestuarioController.get_vestuario_by_id(vestuarioId)

@routerVestuario.post("/create", response_model=dict)
async def create_vestuario(vestuario: dict):
    return await VestuarioController.create_vestuario(vestuario)

@routerVestuario.get("/user/{usuarioId}", response_model=dict)
async def get_vestuario_by_usuario(usuarioId: PydanticObjectId):
    return await VestuarioController.get_vestuario_by_usuario(usuarioId)