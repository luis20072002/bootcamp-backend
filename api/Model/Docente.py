from pydantic import BaseModel,Field

class Docente(BaseModel):
    id : int
    nombre : str
    apellido : str
    correo : str