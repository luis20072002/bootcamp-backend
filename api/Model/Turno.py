from datetime import time
from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base


class Turno(Base):
    __tablename__ = "turnos"

    id_turno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_turno: Mapped[str] = mapped_column(String(20), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)

    planillas: Mapped[list['Planilla']] = relationship(back_populates='turno')
    registros: Mapped[list['Registro']] = relationship(back_populates='turno')
    horarios_auxiliar: Mapped[list['HorarioAuxiliar']] = relationship(
        back_populates='turno_1',
        foreign_keys='HorarioAuxiliar.id_turno_1'
    )
