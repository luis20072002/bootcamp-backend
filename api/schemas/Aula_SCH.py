from pydantic import BaseModel

class AulaCreate(BaseModel):
    id: int
    nombre_aula : str
    edificio : str
    capacidad : int

class AulaResponse(AulaCreate):
    id: int
    class Config:
        from_attributes = True
