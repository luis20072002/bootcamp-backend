from pydantic import BaseModel
from datetime import time


class TurnoCreate(BaseModel):
    nombre_turno: str
    hora_inicio: time
    hora_fin: time


class TurnoResponse(BaseModel):
    id_turno: int
    nombre_turno: str
    hora_inicio: time
    hora_fin: time

    model_config = {"from_attributes": True}


class TurnoUpdate(BaseModel):
    nombre_turno: str | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
