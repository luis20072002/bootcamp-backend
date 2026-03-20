from pydantic import BaseModel
from datetime import date

class PlanillaCreate(BaseModel):

    id_usuario : int
    id_turno : int
    fecha_asignacion : date
    



class PlanillaResponse(BaseModel):
    id: int
    class Config:
        from_attributes = True
    