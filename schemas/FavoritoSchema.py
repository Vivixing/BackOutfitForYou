from beanie import PydanticObjectId
from pydantic import BaseModel

class FavoritoRequest(BaseModel):
    usuarioId: PydanticObjectId
    vestuarioId: PydanticObjectId
