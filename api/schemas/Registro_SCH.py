from pydantic import BaseModel
from datetime import date,time

class RegistroCreate(BaseModel):
    id_turno: int
    id_aula: int
    id_docente : int
    id_curso : str
    asistencia: bool
    uso_medio_solicitudes : bool
    solicitudes : str
    novedades : str

    fecha_registro: date
    hora_registro: time



class RegistroResponse(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True
    