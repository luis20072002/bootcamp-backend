from pydantic import BaseModel
from datetime import date, time
class TurnoCreate(BaseModel):

    id_usuario : int
    fecha : date
    hora_inicio: time
    hora_fin : time
    estado_turno : str

class TurnoResponse(BaseModel):
    id : int

class  TurnoUpdate (BaseModel):
    estado_turno : str