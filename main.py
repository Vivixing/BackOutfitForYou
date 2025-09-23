from routers.RecomendacionRouter import routerRecomendacion as recomendacion_router
from routers.VisualizacionRouter import routerVisualizacion as visualizacion_router
from routers.TipoPrendaRouter import routerTipoPrenda as tipo_prenda_router
from routers.VestuarioRouter import routerVestuario as vestuario_router
from routers.FavoritoRouter import routerFavorito as favorito_router
from routers.PrendaRouter import routerPrenda as prenda_router
from routers.UsuarioRouter import router as usuario_router
from fastapi.middleware.cors import CORSMiddleware
from core.modelLoader import load_h5_model_main
from core.database import init_db
from fastapi import FastAPI
import os

# Inicializar modelo una sola vez
model = None

# Definir lifespan (reemplazo de on_event)
async def lifespan(app: FastAPI):
    global model
    print(">>> Iniciando base de datos y modelo...")
    await init_db()
    model = await load_h5_model_main()
    print(">>> Inicialización completa")
    yield  # <- aquí FastAPI sigue corriendo
    print(">>> Cerrando aplicación...")  # Opcional, al apagar la app

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # <-- or ["*"] para permitir todos
    allow_credentials=True,
    allow_methods=["*"],              # <-- importante para permitir OPTIONS
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(tipo_prenda_router)
app.include_router(prenda_router)
app.include_router(recomendacion_router)
app.include_router(vestuario_router)
app.include_router(visualizacion_router)
app.include_router(favorito_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)