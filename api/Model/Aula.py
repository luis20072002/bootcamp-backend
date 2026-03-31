from sqlalchemy import Column, String, Integer
from api.database.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
class Aula(Base):
    __tablename__ = "aulas"
    id_aula: Mapped[int] = mapped_column(primary_key=True, index=True,autoincrement=True)
    codigo: Mapped[String] = mapped_column(String(10))
    nombre_aula: Mapped[String] = mapped_column(String(100))
    edificio: Mapped[String]= mapped_column(String(100))
    capacidad: Mapped[int] = mapped_column()
    


    #cursos = relationship("Curso", back_populates="aula")
    cursos:Mapped[list['Curso']] = relationship(back_populates='aula')
    registros = relationship("Registro", back_populates="aula")
