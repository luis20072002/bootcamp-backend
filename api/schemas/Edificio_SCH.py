from pydantic import BaseModel


class EdificioCreate(BaseModel):
    nombre: str
    codigo: str
    cantidad_pisos: int


class EdificioResponse(BaseModel):
    id_edificio: int
    nombre: str
    codigo: str
    cantidad_pisos: int
    estado: bool

    model_config = {"from_attributes": True}


class EdificioUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    cantidad_pisos: int | None = None
    estado: bool | None = None
