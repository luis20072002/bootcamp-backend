from sqlalchemy import Column, String, Integer,ForeignKey
from sqlalchemy.orm import relationship
from api.database.database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id_curso = Column(String(255), primary_key=True, index=True)
    nombre_curso = Column(String(100), nullable=False)
    codigo_curso = Column(String(8), nullable=False)
    id_docente = Column(Integer , ForeignKey("docentes.id_docente"))
    id_aula=Column(String(10), ForeignKey("aulas.id_aula"))

    docente = relationship("Docente", back_populates="cursos") 
    aula = relationship("Aula", back_populates="cursos")
    registros = relationship("Registro", back_populates="cursos")
   