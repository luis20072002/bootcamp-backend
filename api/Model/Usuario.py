from pydantic import BaseModel
import hashlib
from datetime import datetime
from model.Role import RoleEnum

class Usuario(BaseModel):
    nombre: str
    pwsd: str
    rol_id: RoleEnum
    estado: bool
    fecha_creacion: datetime

class AuxiliarUpdate(BaseModel):
    nuevo_nombre: str