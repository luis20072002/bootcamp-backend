from sqlalchemy import Column, String, Integer,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.database.database import Base

class Curso(Base):
    __tablename__ = "cursos"

   
    id_curso: Mapped[int] = mapped_column(primary_key=True, index= True)
    nombre_curso: Mapped[String]= mapped_column(String(100), unique=True)
    codi_curso: Mapped[String]= mapped_column(String(8))
    id_docente: Mapped[int]= mapped_column(ForeignKey('docentes.id_docente'))
    id_aula: Mapped[String] = mapped_column(String[10],ForeignKey('aulas.id_aula'))
    id_aula=Column(String(10), ForeignKey("aulas.id_aula"))



    docente: Mapped['Docente']= relationship(back_populates='cursos') 
    aula: Mapped['Aula'] = relationship(back_populates='cursos')
    
    
    registros: Mapped['Registro'] = relationship(back_populates='cursos')