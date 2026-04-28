from typing import Optional
from datetime import date
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base


class HorarioExcepcion(Base):
    __tablename__ = "horario_excepcion"

    id_excepcion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    id_turno_nuevo: Mapped[Optional[int]] = mapped_column(ForeignKey('turnos.id_turno'), nullable=True)
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    id_admin: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)

    usuario: Mapped['Usuario'] = relationship(foreign_keys=[id_usuario], back_populates='excepciones')
    admin: Mapped['Usuario'] = relationship(foreign_keys=[id_admin])
    turno_nuevo: Mapped[Optional['Turno']] = relationship()
