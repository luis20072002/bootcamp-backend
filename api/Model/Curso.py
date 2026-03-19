from pydantic import BaseModel,Field

class CursoCreate(BaseModel):
    id : int
    nombre : str
    codigo : str
    id_docente : int
    estatus: bool #Verifica si está en uso

#CREAR TABLA HORARIO, CURSO AUN NO ESTÁ BIEN
