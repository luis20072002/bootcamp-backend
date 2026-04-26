from sqlalchemy import Column, String, Integer,Time,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base
from datetime import time

class Horario(Base):
    __tablename__="horarios_trabajo"

    id_horario: Mapped[int] = mapped_column(primary_key=True)
    dia_semana: Mapped[String] = mapped_column(String(20), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time,nullable=False)

    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'))
   
    # Relación hacia Usuario (viewonly para evitar conflicto con horario_auxiliar)
    usuario: Mapped['Usuario'] = relationship(foreign_keys=[id_usuario], viewonly=True)


    
