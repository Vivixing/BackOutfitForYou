from fastapi import FastAPI
from core.database import init_db
from core.modelLoader import load_h5_model_main
from routers.UsuarioRouter import router as usuario_router
from routers.TipoPrendaRouter import routerTipoPrenda as tipo_prenda_router
from routers.PrendaRouter import routerPrenda as prenda_router

#Instancia la clase FastAPI
app = FastAPI()
# Inicializar modelo una sola vez
model = None

app.include_router(usuario_router)
app.include_router(tipo_prenda_router)
app.include_router(prenda_router)

#Decorador que indica la ruta de la petición
@app.get("/")
async def get_root():
    await init_db()
    return {"message": "Base de datos inicializada"}

@app.on_event("startup")
async def startup_event():
    global model
    model = await load_h5_model_main()
    return {"message": "Inicializado Modelo"}

