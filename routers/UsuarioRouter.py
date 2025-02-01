from fastapi import APIRouter
from controllers.UsuarioController import UsuarioController
from schemas.UsuarioSchema import UsuarioCreadoRequest, UsuarioLoginRequest
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Usuario"])

@router.post("/register")
async def create_user(request:UsuarioCreadoRequest):
    return await UsuarioController.create_user(request)

@router.post("/login")
async def login_user(request:UsuarioLoginRequest):
    return await UsuarioController.login_user(request)

@router.get("/{user_id}")
async def get_user_by_id(user_id: PydanticObjectId):
    return await UsuarioController.get_user_by_id(user_id)
