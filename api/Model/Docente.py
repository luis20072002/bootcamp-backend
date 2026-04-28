from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..database.database import Base


class Docente(Base):
    __tablename__ = "docentes"

    id_docente: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    telefono: Mapped[str] = mapped_column(String(100))
    estado: Mapped[bool] = mapped_column(default=True, nullable=False)

    cursos: Mapped[list['Curso']] = relationship(back_populates='docente')
    registros: Mapped[list['Registro']] = relationship(back_populates='docente')
