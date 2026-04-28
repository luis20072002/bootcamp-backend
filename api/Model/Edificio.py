from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base


class Edificio(Base):
    __tablename__ = "edificios"

    id_edificio: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    cantidad_pisos: Mapped[int] = mapped_column(nullable=False)
    estado: Mapped[bool] = mapped_column(default=True, nullable=False)

    aulas: Mapped[list['Aula']] = relationship(back_populates='edificio')
    usuarios: Mapped[list['Usuario']] = relationship(back_populates='edificio')
    planillas: Mapped[list['Planilla']] = relationship(back_populates='edificio')
