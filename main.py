from fastapi import FastAPI

#Instancia la clase FastAPI
app = FastAPI()

#Decorador que indica la ruta de la petición
@app.get("/")
def get_root():
    return {"message": "Hello World"}