from fastapi import FastAPI
from core.database import init_db

#Instancia la clase FastAPI
app = FastAPI()

#Decorador que indica la ruta de la petición
@app.get("/")
async def get_root():
    await init_db()
    return {"message": "Database initialized"}