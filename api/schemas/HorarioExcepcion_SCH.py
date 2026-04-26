from pydantic import BaseModel
from datetime import date


class HorarioExcepcionCreate(BaseModel):
    id_usuario: int
    fecha: date
    tipo: str
    id_turno_nuevo: int | None = None
    motivo: str | None = None


class HorarioExcepcionResponse(BaseModel):
    id_excepcion: int
    id_usuario: int
    fecha: date
    tipo: str
    id_turno_nuevo: int | None
    motivo: str | None
    id_admin: int

    model_config = {"from_attributes": True}
