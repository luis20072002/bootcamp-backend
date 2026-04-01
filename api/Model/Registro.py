from sqlalchemy import Column, String, Integer,Boolean,ForeignKey, Date, Time
from sqlalchemy.orm import relationship, mapped_column,Mapped
from api.database.database import Base
from datetime import date,time


class Registro(Base):
    __tablename__= "registros_aula"


    id_registro: Mapped[int] = mapped_column(primary_key=True)
    asistencia_docente: Mapped[bool] = mapped_column()
    uso_medios_audiovisuales: Mapped[bool] = mapped_column()
    solicitudes: Mapped[String] = mapped_column(String(300),nullable=True)
    novedades: Mapped[String] = mapped_column(String(300), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date,nullable=False)
    hora_registro: Mapped[time] = mapped_column(Time,nullable=False)
  

    id_turno: Mapped[int] = mapped_column(ForeignKey('turnos.id_turno'))
    id_aula: Mapped[int] = mapped_column(ForeignKey('aulas.id_aula'))
    id_docente: Mapped[int] = mapped_column(ForeignKey('docentes.id_docente'))
    id_curso: Mapped[int] = mapped_column(ForeignKey('cursos.id_curso'))
   

    turnos: Mapped[list['Turno']]= relationship(back_populates='registros')
    aula: Mapped[list['Aula']] = relationship(back_populates='registros')
    docente: Mapped[list['Docente']]= relationship(back_populates='registros')
    cursos: Mapped[list['Curso']] = relationship(back_populates='registros')

    
    
