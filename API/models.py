from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "USUARIOS"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)