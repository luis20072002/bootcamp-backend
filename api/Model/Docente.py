from sqlalchemy import Column, String
from sqlalchemy.orm import relationship,mapped_column,Mapped
from api.database.database import Base

class Docente(Base):
    __tablename__ = "docentes"
  
    id_docente: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[String] = mapped_column(String(100))
    apellido: Mapped[String] = mapped_column(String(100))
    correo: Mapped[String] = mapped_column(String(100), unique=True)
    telefono: Mapped[String] = mapped_column(String(100))
    
   

   
   
    cursos: Mapped[list['Curso']] = relationship(back_populates='docente')    
    registros: Mapped['Registro'] = relationship(back_populates='docente')  