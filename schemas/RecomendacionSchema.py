from pydantic import BaseModel, Field, field_validator

class RecomendacionRequest(BaseModel):
    ocasion: str = Field(..., max_length=1000)

    @field_validator('ocasion', mode='before')
    @classmethod
    def validar_ocasion(cls, infoOcasion):
        if not infoOcasion:
            raise ValueError('La ocasión es requerida')
        if not infoOcasion.strip():
            raise ValueError('La ocasión no puede estar vacía')
        if len(infoOcasion) > 1000:
            raise ValueError('La ocasión no puede exceder los 100 caracteres')
        return infoOcasion.capitalize()