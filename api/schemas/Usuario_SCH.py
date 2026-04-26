from pydantic import BaseModel
from datetime import datetime
from api.schemas.Rol_SCH import RolResponse


class UsuarioCreate(BaseModel):
    nombre: str
    pwsd: str
    estado: bool
    rol_id: int
    correo: str
    id_edificio: int | None = None


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    estado: bool
    fecha_creacion: datetime
    rol: RolResponse
    id_edificio: int | None = None

    model_config = {
        "from_attributes": True
    }


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    pwsd: str | None = None
    estado: bool | None = None
    rol_id: int | None = None
    id_edificio: int | None = None
