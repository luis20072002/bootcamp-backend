from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database.database import Base


class Aula(Base):
    __tablename__ = "aulas"

    id_aula: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(10))
    nombre_aula: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    piso: Mapped[int] = mapped_column(nullable=False)
    capacidad: Mapped[int] = mapped_column()
    id_edificio: Mapped[int] = mapped_column(ForeignKey('edificios.id_edificio'), nullable=False)

    edificio: Mapped['Edificio'] = relationship(back_populates='aulas')
    cursos: Mapped[list['Curso']] = relationship(back_populates='aula')
    registros: Mapped[list['Registro']] = relationship(back_populates='aula')
