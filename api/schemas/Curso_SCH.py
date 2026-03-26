from pydantic import BaseModel

class CursoCreate(BaseModel):
    id_curso: str
    nombre_curso: str
    codi_curso: str
    id_docente: int
    id_aula: str

class CursoResponse(BaseModel):
    id_curso: str
    nombre_curso: str
    codi_curso: str
    id_docente: int
    id_aula: str

    model_config = {"from_attributes": True}