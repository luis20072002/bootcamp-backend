from pydantic import BaseModel
from datetime import datetime
class UsuarioCreate(BaseModel):
    
    
    id: int
    nombre: str
    pwsd : str
    estado : bool
    fecha_creacion: datetime
    ultimo_login: datetime
    rol_id: int

class UsuarioResponse(BaseModel):
    id: int
    nombre: int
    ultimo_login : datetime








