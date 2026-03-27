from pydantic import BaseModel, field_validator
import re

PATRON_AULA = re.compile(r'^A[1-9]-[1-9](0[1-9]|1[0-9]|20)$')

class AulaCreate(BaseModel):
    codigo: str
    nombre: str | None = None
    edificio: str
    capacidad: int

    @field_validator('codigo')
    @classmethod
    def validar_formato_codigo(cls, v: str) -> str:
        if not PATRON_AULA.match(v):
            raise ValueError(
                "El codigo debe tener el formato A{edificio}-{piso}{salon}. "
                "Ejemplo: A5-202. Edificio: 1-9, Piso: 1-9, Salon: 01-20."
            )
        return v.upper()

class AulaResponse(BaseModel):
    id_aula: int
    codigo: str
    nombre: str | None
    edificio: str
    capacidad: int

    model_config = {"from_attributes": True}