from datetime import datetime
from sqlalchemy import Column,Integer,VARBINARY, Boolean, DateTime,ForeignKey, String
from api.database.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Usuario(Base):
    __tablename__="usuario"
    id_usuario:  Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[String] = mapped_column(String(50),nullable=False)
    pwsd: Mapped[String] = mapped_column(String(255), nullable=False)
    estado: Mapped[bool] = mapped_column(default=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    ultima_actividad: Mapped[datetime]= mapped_column(DateTime,nullable=False)  
    correo: Mapped[String] = mapped_column(String(100),unique=True, nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey('ROL.rol_id'))
    
    rol: Mapped['Rol'] = relationship(back_populates='usuarios')
   
    planillas = relationship("Planilla",back_populates="usuario")
    horario = relationship("Horario",back_populates="usuario")


 