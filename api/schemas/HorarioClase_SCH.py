from pydantic import BaseModel
from datetime import time


class HorarioClaseCreate(BaseModel):
    id_planilla: int
    id_aula: int
    id_docente: int
    id_curso: int
    hora_inicio: time
    hora_fin: time
    dia_semana: int | None = None


class HorarioClaseResponse(BaseModel):
    id_horario_clase: int
    id_planilla: int
    id_aula: int
    id_docente: int
    id_curso: int
    hora_inicio: time
    hora_fin: time
    dia_semana: int | None

    model_config = {"from_attributes": True}


class HorarioClaseUpdate(BaseModel):
    id_aula: int | None = None
    id_docente: int | None = None
    id_curso: int | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    dia_semana: int | None = None
