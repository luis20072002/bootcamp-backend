<<<<<<< HEAD
from pydantic import BaseModel,Field

class Aula(BaseModel):
    codigo: str = Field(pattern=r"^A[1-5]-[1-6](0[1-9]|1[0-9]|20)$")
    nombre: str | None = None
    edificio: str
    capacidad: int
=======
from sqlalchemy import Column, String, Integer
from api.database.database import Base
from sqlalchemy.orm import relationship
class Aula(Base):
    __tablename__ = "aulas"

    id_aula = Column(String(10), primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)
    edificio = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)

    cursos = relationship("Curso", back_populates="aula")
    registros = relationship("Registro",back_populates="aulas")
>>>>>>> API_DEBUG
