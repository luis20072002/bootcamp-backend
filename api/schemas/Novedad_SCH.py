from pydantic import BaseModel
from datetime import datetime


class NovedadCreate(BaseModel):
    id_registro: int
    descripcion: str


class NovedadResponse(BaseModel):
    id_novedad: int
    id_registro: int
    descripcion: str
    fecha_novedad: datetime

    model_config = {"from_attributes": True}


class NovedadDetalleResponse(BaseModel):
    id_novedad:      int
    id_registro:     int
    descripcion:     str
    fecha_novedad:   datetime
 
    # Aula
    id_aula:         int
    aula_codigo:     str
    aula_nombre:     str | None   # puede ser NULL en BD
    piso:            int
 
    # Edificio
    id_edificio:     int
    nombre_edificio: str
 
    # Auxiliar
    id_usuario:      int
    auxiliar_nombre: str
 
    model_config = {"from_attributes": True}