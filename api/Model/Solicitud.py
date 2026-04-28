from typing import Optional
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id_solicitud: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_registro: Mapped[int] = mapped_column(ForeignKey('registros_aula.id_registro'), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default='pendiente')
    nota_resolucion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resuelta_por_auxiliar: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    fecha_solicitud: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_resolucion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    registro: Mapped['Registro'] = relationship(back_populates='solicitudes')
