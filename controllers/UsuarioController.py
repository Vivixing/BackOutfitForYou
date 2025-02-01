from services.UsuarioService import UsuarioService
from schemas.UsuarioSchema import UsuarioCreadoRequest, UsuarioLoginRequest
from fastapi import HTTPException
from beanie import PydanticObjectId

async def create_user(request:UsuarioCreadoRequest):
    try:
        user = await UsuarioService.create_user(request)
        return {"status": 200, "message": "Usuario creado correctamente", "user_id":str(user.id), "data": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def login_user(request:UsuarioLoginRequest):
    try:
        user = await UsuarioService.login_user(request.email, request.contrasena)
        return {"status": 200, "message": "Usuario logueado correctamente", "user_id":str(user.id), "data": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
async def get_user_by_id(user_id:PydanticObjectId):
    try:
        user = await UsuarioService.find_user_by_id(user_id)
        return {"status": 200, "message": "Usuario encontrado", "data": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))