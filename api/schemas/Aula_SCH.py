from pydantic import BaseModel

class AulaCreate(BaseModel):
    id_aula: str
    nombre_aula: str
    edificio: str
    capacidad: int

class AulaResponse(BaseModel):
    id_aula: str
    nombre_aula: str | None
    edificio: str
    capacidad: int

    model_config = {"from_attributes": True}