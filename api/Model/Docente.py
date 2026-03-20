from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from api.database.database import Base

class Docente(Base):
    __tablename__ = "docentes"
    id_docente = Column(Integer , primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo =  Column(String(100), nullable=False, unique=True)
    telefono =  Column(String(100), nullable=False)
    cursos = relationship("Curso",back_populates="docente")
    
   

registros = relationship("Registro",back_populates="docentes")