from pydantic import BaseModel
import hashlib
from datetime import datetime
from Model.Role import Role

class Usuario(BaseModel):
    nombre: str
    pwsd: str
    rol: Role
    estado: bool
    fecha_creacion: datetime
    Ultimo_login: datetime

class UsuarioUpdate(BaseModel):
    nuevo_nombre: str