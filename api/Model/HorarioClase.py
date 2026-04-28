from typing import Optional
from datetime import time
from sqlalchemy import Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base


class HorarioClase(Base):
    __tablename__ = "horario_clase"

    id_horario_clase: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_planilla: Mapped[int] = mapped_column(ForeignKey('planilla_trabajo.id_planillas'), nullable=False)
    id_aula: Mapped[int] = mapped_column(ForeignKey('aulas.id_aula'), nullable=False)
    id_docente: Mapped[int] = mapped_column(ForeignKey('docentes.id_docente'), nullable=False)
    id_curso: Mapped[int] = mapped_column(ForeignKey('cursos.id_curso'), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    dia_semana: Mapped[Optional[int]] = mapped_column(nullable=True)

    planilla: Mapped['Planilla'] = relationship(back_populates='clases')
    aula: Mapped['Aula'] = relationship()
    docente: Mapped['Docente'] = relationship()
    curso: Mapped['Curso'] = relationship()
