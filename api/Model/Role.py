from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from ..database.database import Base
class Rol(Base):
    __tablename__ = "ROL"

    rol_id: Mapped[int]= mapped_column(primary_key=True)
    nombre_rol: Mapped[String] = mapped_column(String(100),nullable=False)
   

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")
  