from sqlalchemy import Column, Integer, DateTime,ForeignKey
from api.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
class Planilla(Base):
    __tablename__="planilla_trabajo"
    id_planillas: Mapped[int] = mapped_column(primary_key=True)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime, nullable= False)
 
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'))
    id_turno: Mapped[int] = mapped_column(ForeignKey('turnos.id_turno'))
    
    usuario: Mapped['Usuario'] = relationship(back_populates='planillas')
    turno: Mapped['Turno'] = relationship(back_populates='planillas')