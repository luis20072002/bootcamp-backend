
from sqlalchemy import Column,Integer,VARBINARY, Boolean, DateTime,ForeignKey, String
from database.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__="usuario"
    id_usuario = Column(Integer,primary_key=True)
    nombre = Column(String(50), nullable=False)
    pwsd = Column (String(255), nullable=False)
    estado = Column(Boolean,default=True, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    ultima_actividad =  Column(DateTime, nullable=False)
    rol_id = Column(Integer,ForeignKey("roles.rol_id"))

    rol = relationship("Rol",back_populates="usuarios")
    turnos = relationship("Turno",back_populates="usuarios")
    planillas = relationship("Planilla",back_populates="usuario")
    horario = relationship("Horario",back_populates="usuario")
