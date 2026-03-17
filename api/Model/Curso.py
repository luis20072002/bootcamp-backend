from pydantic import BaseModel,Field

class Curso(BaseModel):
    id : int
    nombre : str
    codigo : str
    id_docente : int