from pydantic import BaseModel
from datetime import time

class HorarioCreate(BaseModel):
    id_usuario : int
    dia_semana: str
    hora_inicio : time
    hora_fin : time    


class HorarioResponse(BaseModel):
    id: int
    class Config:
        from_attributes = True
    