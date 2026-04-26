from pydantic import BaseModel
from datetime import datetime


class NovedadCreate(BaseModel):
    id_registro: int
    descripcion: str


class NovedadResponse(BaseModel):
    id_novedad: int
    id_registro: int
    descripcion: str
    fecha_novedad: datetime

    model_config = {"from_attributes": True}
