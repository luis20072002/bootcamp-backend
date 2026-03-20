from pydantic import BaseModel

class DocenteCreate(BaseModel):
    id: int
    nombre: str
    apellido : str
    correo : str
    telefono : str

class DocenteResponse(DocenteCreate):
    id: int
    class Config:
        from_attributes = True

class DocenteUpdate(BaseModel):
    id: int

    