<<<<<<< HEAD
from pydantic import BaseModel
import hashlib
from datetime import date,time
from Model.Role import Role

class Usuario(BaseModel):
    nombre: str
    pwsd: str
    rol: Role
    estado: bool
    fecha_creacion: date
    Ultimo_login: date

class UsuarioUpdate(BaseModel):
    nuevo_nombre: str
=======

from sqlalchemy import Column,Integer,VARBINARY, Boolean, DateTime,ForeignKey
from api.database.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__="usuario"
    id_usuario = Column(Integer,primary_key=True)
    password = Column (VARBINARY(255), nullable=False)
    estado = Column(Boolean,default=True, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    ultima_actividad =  Column(DateTime, nullable=False)
    rol_id = Column(Integer,ForeignKey("roles.rol_id"))

    rol = relationship("Rol",back_populates="usuarios")
    turnos = relationship("Turno",back_populates="usuarios")
    planillas = relationship("Planilla",back_populates="usuario")
    horario = relationship("Horario",back_populates="usuario")
>>>>>>> API_DEBUG
