from sqlalchemy import Column, String, Integer,Boolean,ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from database.database import Base


class Registro(Base):
    __tablename__= "registros_aula"

    id_registro = Column(Integer,primary_key=True)
    asistencia_docente = Column(Boolean, nullable=False)
    uso_medios_audiovisuales = Column(Boolean,nullable=False)
    solicitudes = Column(String(300), nullable=True)
    novedades = Column((300), nullable=True)
    fecha_registro= Column(Date, nullable=False)
    hora_registro = Column(Time, nullable=False)


    id_turno = Column(Integer, ForeignKey("turnos.id_turno"))
    id_aula = Column(Integer, ForeignKey("aulas.id_aula"))
    id_docente = Column(Integer, ForeignKey("docentes.id_docente"))
    id_curso = Column(String(255), ForeignKey("cursos.id_curso"))


    turnos = relationship("Turno",back_populates="registros")
    aulas = relationship("Aula",back_populates="registros")
    docentes = relationship("Docente",back_populates="registros")
    cursos = relationship("Curso",back_populates="registros")
    
    
