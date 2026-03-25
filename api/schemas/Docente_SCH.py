from pydantic import BaseModel

class DocenteCreate(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: str

class DocenteResponse(BaseModel):
    id_docente: int
    nombre: str
    apellido: str
    correo: str
    telefono: str

    model_config = {"from_attributes": True}