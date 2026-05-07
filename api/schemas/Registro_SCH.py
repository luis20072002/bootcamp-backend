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


class RegistroDetalleResponse(BaseModel):
    id_registro:              int
    asistencia_docente:       bool
    uso_medios_audiovisuales: bool
    fecha_registro:           date
    hora_registro:            time

    # Turno
    id_turno:     int
    nombre_turno: str

    # Aula
    id_aula:    int
    aula_codigo: str
    nombre_aula: str | None

    # Edificio (via aula)
    id_edificio:     int
    nombre_edificio: str
    piso:            int

    # Docente
    id_docente:       int
    docente_nombre:   str
    docente_apellido: str

    # Curso
    id_curso:    int
    curso_nombre: str

    # Auxiliar
    id_usuario:      int
    auxiliar_nombre: str

    model_config = {"from_attributes": True}