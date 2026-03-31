from sqlalchemy import Column, String, Integer,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.database.database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id_curso = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(100), nullable=False, unique=True)
    codi_curso = Column(String(8), nullable=False)
    id_docente = Column(Integer , ForeignKey("docentes.id_docente"))
    id_aula=Column(String(10), ForeignKey("aulas.id_aula"))

   
    docente: Mapped['Docente']= relationship(back_populates='cursos') 
    aula: Mapped['Aula'] = relationship(back_populates='cursos')
    #aula = relationship("Aula", back_populates="cursos")
    registros = relationship("Registro", back_populates="cursos")
   