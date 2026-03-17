from pydantic import BaseModel,Field
from datetime import date, time
class Turno(BaseModel):
    id : int
    fecha : date
    hora_inicio : time
    hora_fin : time
    estado_turno : bool