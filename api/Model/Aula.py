from pydantic import BaseModel,Field

class Aula(BaseModel):
    codigo: str = Field(pattern=r"^A[1-5]-[1-6](0[1-9]|1[0-9]|20)$")
    nombre: str | None = None
    edificio: str
    capacidad: int