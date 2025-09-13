from pydantic import BaseModel

class FavoritoRequest(BaseModel):
    usuarioId: str
    vestuarioId: str
