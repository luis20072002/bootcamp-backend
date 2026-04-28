from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from ..database.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    pwsd: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[bool] = mapped_column(default=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ultima_actividad: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey('ROL.rol_id'))
    id_edificio: Mapped[Optional[int]] = mapped_column(ForeignKey('edificios.id_edificio'), nullable=True)

    rol: Mapped['Rol'] = relationship(back_populates='usuarios')
    edificio: Mapped[Optional['Edificio']] = relationship(back_populates='usuarios')
    planillas: Mapped[list['Planilla']] = relationship(back_populates='usuario')
    horario_auxiliar: Mapped[list['HorarioAuxiliar']] = relationship(back_populates='usuario')
    excepciones: Mapped[list['HorarioExcepcion']] = relationship(
        back_populates='usuario',
        foreign_keys='HorarioExcepcion.id_usuario'
    )
    registros: Mapped[list['Registro']] = relationship(back_populates='usuario')
