from sqlalchemy import Column, String, Integer
from database.database import Base
from sqlalchemy.orm import relationship
class Aula(Base):
    __tablename__ = "aulas"

    id_aula = Column(String(10), primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)
    edificio = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)

    cursos = relationship("Curso", back_populates="aula")
    registros = relationship("Registro", back_populates="aula")
