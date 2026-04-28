from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base


class HorarioAuxiliar(Base):
    __tablename__ = "horario_auxiliar"

    id_horario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)
    dia_semana: Mapped[int] = mapped_column(nullable=False)
    id_turno_1: Mapped[int] = mapped_column(ForeignKey('turnos.id_turno'), nullable=False)
    id_turno_2: Mapped[Optional[int]] = mapped_column(ForeignKey('turnos.id_turno'), nullable=True)
    periodo_vigencia: Mapped[str] = mapped_column(String(10), nullable=False)

    usuario: Mapped['Usuario'] = relationship(back_populates='horario_auxiliar')
    turno_1: Mapped['Turno'] = relationship(foreign_keys=[id_turno_1], back_populates='horarios_auxiliar')
    turno_2: Mapped[Optional['Turno']] = relationship(foreign_keys=[id_turno_2])
