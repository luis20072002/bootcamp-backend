from pydantic import BaseModel
from datetime import date, datetime


class PlanillaCreate(BaseModel):
    id_usuario: int
    id_turno: int
    id_edificio: int
    piso_1: int
    piso_2: int | None = None
    piso_3: int | None = None
    periodo_vigencia: str
    fecha_asignacion: date


class PlanillaResponse(BaseModel):
    id_planillas: int
    id_usuario: int
    id_turno: int
    id_edificio: int
    piso_1: int
    piso_2: int | None
    piso_3: int | None
    periodo_vigencia: str
    estado: str
    fecha_asignacion: datetime

    model_config = {"from_attributes": True}


class PlanillaUpdate(BaseModel):
    estado: str | None = None
    piso_1: int | None = None
    piso_2: int | None = None
    piso_3: int | None = None
