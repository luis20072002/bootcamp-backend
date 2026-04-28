from datetime import date, time
from sqlalchemy import ForeignKey, Date, Time
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..database.database import Base


class Registro(Base):
    __tablename__ = "registros_aula"

    id_registro: Mapped[int] = mapped_column(primary_key=True)
    asistencia_docente: Mapped[bool] = mapped_column()
    uso_medios_audiovisuales: Mapped[bool] = mapped_column()
    fecha_registro: Mapped[date] = mapped_column(Date, nullable=False)
    hora_registro: Mapped[time] = mapped_column(Time, nullable=False)

    id_turno: Mapped[int] = mapped_column(ForeignKey('turnos.id_turno'))
    id_aula: Mapped[int] = mapped_column(ForeignKey('aulas.id_aula'))
    id_docente: Mapped[int] = mapped_column(ForeignKey('docentes.id_docente'))
    id_curso: Mapped[int] = mapped_column(ForeignKey('cursos.id_curso'))
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario'), nullable=False)

    turno: Mapped['Turno'] = relationship(back_populates='registros')
    aula: Mapped['Aula'] = relationship(back_populates='registros')
    docente: Mapped['Docente'] = relationship(back_populates='registros')
    cursos: Mapped['Curso'] = relationship(back_populates='registros')
    usuario: Mapped['Usuario'] = relationship(back_populates='registros')
    novedades: Mapped[list['Novedad']] = relationship(back_populates='registro')
    solicitudes: Mapped[list['Solicitud']] = relationship(back_populates='registro')
