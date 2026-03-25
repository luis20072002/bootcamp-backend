from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from api.database.database import Base

class Rol(Base):
    __tablename__ = "ROL"

    rol_id = Column(Integer, primary_key=True)
    nombre_rol = Column(String(50), nullable=False)

  
    usuarios = relationship("Usuario", back_populates="rol")