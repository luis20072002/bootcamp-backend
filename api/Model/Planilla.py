from sqlalchemy import Column, Integer, DateTime,ForeignKey
from api.database.database import Base
from sqlalchemy.orm import relationship

class Planilla(Base):
    __tablename__="planilla_trabajo"
    id_planillas = Column(Integer,primary_key=True)
    fecha_asignacion = Column(DateTime, nullable=False)
 
    id_usuario = Column(Integer,ForeignKey("usuario.id_usuario"))
    id_turno = Column(Integer,ForeignKey("turnos.id_turno"))

    usuario = relationship("Usuario",back_populates="planillas")
    turno = relationship("Turno",back_populates="planillas")