from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base


class HistorialEdificioAuxiliar(Base):
    __tablename__ = "historial_edificio_auxiliar"

    id_historial: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)
    id_edificio_anterior: Mapped[Optional[int]] = mapped_column(ForeignKey('edificios.id_edificio'), nullable=True)
    id_edificio_nuevo: Mapped[int] = mapped_column(ForeignKey('edificios.id_edificio'), nullable=False)
    fecha_cambio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    id_admin: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)

    usuario: Mapped['Usuario'] = relationship(foreign_keys=[id_usuario])
    edificio_anterior: Mapped[Optional['Edificio']] = relationship(foreign_keys=[id_edificio_anterior])
    edificio_nuevo: Mapped['Edificio'] = relationship(foreign_keys=[id_edificio_nuevo])
    admin: Mapped['Usuario'] = relationship(foreign_keys=[id_admin])
