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


app = FastAPI()

# Inicializar modelo una sola vez
model = None

# Lista de orígenes permitidos
origins = [
    "http://localhost:8100",  # frontend Ionic
]

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

@app.on_event("startup")
async def startup_event():
    global model
    await init_db() 
    model = await load_h5_model_main()
    return {"message": "Inicialización completa"}

