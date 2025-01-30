from beanie import Document, Link
from typing import List
from pydantic import EmailStr
from models.PrendaModel import Prenda
from models.FavoritoModel import Favorito

class Usuario(Document):
    nombre: str
    email: EmailStr
    contrasena: str
    closet: List[Link[Prenda]]=[]
    favoritos: List[Link[Favorito]]=[]

    class Settings:
        collection = "usuarios"
