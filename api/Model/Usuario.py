from pydantic import BaseModel
import hashlib
from datetime import date,time
from Model.Role import Role

class Usuario(BaseModel):
    nombre: str
    pwsd: str
    rol: Role
    estado: bool
    fecha_creacion: date
    Ultimo_login: date

class UsuarioUpdate(BaseModel):
    nuevo_nombre: str