from pydantic import BaseModel
from datetime import date, time

class TurnoCreate(BaseModel):
    id_usuario: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado_turno: str

class TurnoResponse(BaseModel):
    id_turno: int
    id_usuario: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado_turno: str

    model_config = {"from_attributes": True}

class TurnoUpdate(BaseModel):
    estado_turno: str