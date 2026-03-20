from pydantic import BaseModel
from datetime import datetime
class UsuarioCreate(BaseModel):
    nombre: str
    pwsd : str
    estado : bool
    rol_id: int

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    estado: bool
    fecha_creacion: datetime
    rol_id: int

    model_config = {
        "from_attributes": True
    }
        
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    pwsd: str | None = None
    estado: bool | None = None
    rol_id: int | None = None






