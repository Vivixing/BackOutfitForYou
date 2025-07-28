from typing import List
from beanie import PydanticObjectId
from pydantic import BaseModel, Field

class VestuarioRequest(BaseModel):
    usuarioId: PydanticObjectId = Field(...)
    prendas: List[str] = []
    ocasion: str