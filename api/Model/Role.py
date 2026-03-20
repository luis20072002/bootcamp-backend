from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.database import Base

class Rol(Base):
    __tablename__ = "roles"

    rol_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

  
<<<<<<< HEAD
    usuarios = relationship("Usuario",back_populates="rol")
=======
    usuarios = relationship("Usuario",back_populates="roles")
>>>>>>> luiapi
