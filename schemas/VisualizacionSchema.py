from pydantic import BaseModel, Field

class Person(BaseModel):
    hay_persona: bool = Field (..., description="Whether the first image contains a person")
    descripcion: str = Field(..., description="Description of the person in the image")

class ClothingItem(BaseModel):
    hay_prendas: bool = Field(..., description="Whether this image is a clothing item")
    tipo_prenda: str = Field(..., description="Type of clothing (e.g. shirt, pants)")

class VisualizacionCreateRequest(BaseModel):
    usuarioId: str
    vestuarioId: str
    imagen_visualizacion: str