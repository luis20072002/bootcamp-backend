from pydantic import BaseModel
from datetime import datetime


class SolicitudCreate(BaseModel):
    id_registro: int
    descripcion: str


class SolicitudResponse(BaseModel):
    id_solicitud: int
    id_registro: int
    descripcion: str
    estado: str
    nota_resolucion: str | None
    resuelta_por_auxiliar: bool | None
    fecha_solicitud: datetime
    fecha_resolucion: datetime | None

    model_config = {"from_attributes": True}


class SolicitudUpdateEstado(BaseModel):
    estado: str
    nota_resolucion: str | None = None
