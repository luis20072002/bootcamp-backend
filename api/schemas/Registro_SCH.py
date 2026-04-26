from pydantic import BaseModel
from datetime import date, time


class RegistroCreate(BaseModel):
    id_turno: int
    id_aula: int
    id_docente: int
    id_curso: int
    asistencia_docente: bool
    uso_medios_audiovisuales: bool
    fecha_registro: date
    hora_registro: time


class RegistroResponse(BaseModel):
    id_registro: int
    id_turno: int
    id_aula: int
    id_docente: int
    id_curso: int
    id_usuario: int
    asistencia_docente: bool
    uso_medios_audiovisuales: bool
    fecha_registro: date
    hora_registro: time

    model_config = {"from_attributes": True}
