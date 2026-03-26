from pydantic import BaseModel
from datetime import datetime
from api.schemas.Rol_SCH import RolResponse  # importas el schema de Rol


class UsuarioCreate(BaseModel):
    nombre: str
    pwsd: str
    estado: bool
    rol_id: int


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    estado: bool
    fecha_creacion: datetime
    rol: RolResponse          # objeto completo en lugar de solo el id

    model_config = {
        "from_attributes": True
    }


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    pwsd: str | None = None
    estado: bool | None = None
    rol_id: int | None = None