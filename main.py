from fastapi import FastAPI
from core.database import init_db
from routers.UsuarioRouter import router as usuario_router

#Instancia la clase FastAPI
app = FastAPI()

app.include_router(usuario_router)

#Decorador que indica la ruta de la petición
@app.get("/")
async def get_root():
    await init_db()
    return {"message": "Base de datos inicializada"}