from sqlalchemy import Column, String, Integer,Date,Time,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.database.database import Base
from datetime import date,time
class Turno(Base):
    __tablename__= "turnos"

    id_turno: Mapped[int] = mapped_column(primary_key=True)
    
    fecha = Column(Date, nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin:Mapped[time] = mapped_column(Time, nullable=False)
    estado_turno: Mapped[String]= mapped_column(String(40))
    
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'))
   
    planillas: Mapped[list['Planilla']]= relationship(back_populates='turno')
    
    registros: Mapped['Registro'] = relationship(back_populates='turnos')
    
