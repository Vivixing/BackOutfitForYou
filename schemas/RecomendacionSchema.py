from pydantic import BaseModel, Field
from typing import List

class RecomendacionRequest(BaseModel):
    usuarioId: str = Field(..., description="ID del usuario que solicita la recomendación")
    ocasion: str = Field(..., description="Descripción de la ocasión o evento")
    
class RecomendacionResponse(BaseModel):
    id: str
    usuarioId: str
    ocasion: str
    vestuarioSugerido: List[str]
    fechaCreado: str
