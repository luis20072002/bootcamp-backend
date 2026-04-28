from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base


class Planilla(Base):
    __tablename__ = "planilla_trabajo"

    id_planillas: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'))
    id_turno: Mapped[int] = mapped_column(ForeignKey('turnos.id_turno'))
    id_edificio: Mapped[int] = mapped_column(ForeignKey('edificios.id_edificio'), nullable=False)

    piso_1: Mapped[int] = mapped_column(nullable=False)
    piso_2: Mapped[Optional[int]] = mapped_column(nullable=True)
    piso_3: Mapped[Optional[int]] = mapped_column(nullable=True)
    periodo_vigencia: Mapped[str] = mapped_column(String(10), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default='activa')

    usuario: Mapped['Usuario'] = relationship(back_populates='planillas')
    turno: Mapped['Turno'] = relationship(back_populates='planillas')
    edificio: Mapped['Edificio'] = relationship(back_populates='planillas')
    clases: Mapped[list['HorarioClase']] = relationship(back_populates='planilla')
