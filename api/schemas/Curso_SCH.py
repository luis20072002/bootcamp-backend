from pydantic import BaseModel

class CursoCreate(BaseModel):
    nombre_curso: str
    codi_curso: str
    id_docente: int
    id_aula: int

class CursoResponse(BaseModel):
    id_curso: int
    nombre_curso: str
    codi_curso: str
    id_docente: int
    id_aula: str
    
    #model_config = {"from_attributes": True}
    class Config:
        from_attributes = True