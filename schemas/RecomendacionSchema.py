from pydantic import BaseModel, Field
from typing import List

class RecomendacionRequest(BaseModel):
    usuarioId: str = Field(...)
    ocasion: str = Field(...)
    vestuarioSugerido: List[str] = Field(...)

