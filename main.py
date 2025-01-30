from fastapi import FastAPI
from core.database import init_db

#Instancia la clase FastAPI
app = FastAPI()

#Decorador que indica que se ejecutará antes de la primera petición
@app.on_event("startup")
async def startup_event():  
    #Inicializa la base de datos
    await init_db()
    
#Decorador que indica la ruta de la petición
@app.get("/")
def get_root():
    return {"message": "Hello World"}