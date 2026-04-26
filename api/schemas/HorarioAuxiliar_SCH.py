from pydantic import BaseModel, field_validator


class HorarioAuxiliarCreate(BaseModel):
    id_usuario: int
    dia_semana: int
    id_turno_1: int
    id_turno_2: int | None = None
    periodo_vigencia: str

    @field_validator('dia_semana')
    @classmethod
    def validar_dia(cls, v):
        if not 1 <= v <= 7:
            raise ValueError("dia_semana debe estar entre 1 (Lunes) y 7 (Domingo)")
        return v


class HorarioAuxiliarResponse(BaseModel):
    id_horario: int
    id_usuario: int
    dia_semana: int
    id_turno_1: int
    id_turno_2: int | None
    periodo_vigencia: str

    model_config = {"from_attributes": True}


class HorarioAuxiliarUpdate(BaseModel):
    dia_semana: int | None = None
    id_turno_1: int | None = None
    id_turno_2: int | None = None
    periodo_vigencia: str | None = None

    @field_validator('dia_semana')
    @classmethod
    def validar_dia(cls, v):
        if v is not None and not 1 <= v <= 7:
            raise ValueError("dia_semana debe estar entre 1 (Lunes) y 7 (Domingo)")
        return v
