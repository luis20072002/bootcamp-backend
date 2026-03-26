from pydantic import BaseModel
from datetime import date, datetime

class PlanillaCreate(BaseModel):
    id_usuario: int
    id_turno: int
    fecha_asignacion: date

class PlanillaResponse(BaseModel):
    id_planillas: int
    id_usuario: int
    id_turno: int
    fecha_asignacion: datetime

    model_config = {"from_attributes": True}