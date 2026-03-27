from sqlalchemy import Column, String, Integer,Date,Time,ForeignKey
from sqlalchemy.orm import relationship
from api.database.database import Base

class Turno(Base):
    __tablename__= "turnos"

    id_turno = Column(Integer, primary_key=True)
    
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado_turno = Column(String(40), nullable=False )

    id_usuario =  Column(Integer,ForeignKey("usuario.id_usuario"))

    planillas = relationship("Planilla",back_populates="turno")

    registros= relationship("Registro",back_populates="turnos")
