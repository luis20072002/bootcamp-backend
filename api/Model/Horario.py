from sqlalchemy import Column, String, Integer,Time,ForeignKey
from sqlalchemy.orm import relationship
from api.database.database import Base


class Horario(Base):
    __tablename__="horarios_trabajo"

    id_horario = Column(Integer, primary_key=True)

    dia_semana = Column(String(20), nullable=False)
    hora_inicio = Column(Time, nullable= False)
    hora_fin = Column(Time,nullable=False)

    id_usuario = Column(Integer,ForeignKey("usuario.id_usuario"))

    usuario = relationship("Usuario",back_populates="horario")

