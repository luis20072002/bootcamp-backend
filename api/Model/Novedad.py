from datetime import datetime
from sqlalchemy import DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base


class Novedad(Base):
    __tablename__ = "novedades"

    id_novedad: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_registro: Mapped[int] = mapped_column(ForeignKey('registros_aula.id_registro'), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_novedad: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    registro: Mapped['Registro'] = relationship(back_populates='novedades')
