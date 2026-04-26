from pydantic import BaseModel
from datetime import datetime


class HistorialEdificioAuxiliarResponse(BaseModel):
    id_historial: int
    id_usuario: int
    id_edificio_anterior: int | None
    id_edificio_nuevo: int
    fecha_cambio: datetime
    id_admin: int

    model_config = {"from_attributes": True}
