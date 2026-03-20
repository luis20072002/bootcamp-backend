from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pyodbc
DATABASE_URL = "mssql+pyodbc://talento:cartagena@nodossolutions.com:1435/SGS?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()  # abre la sesión
    try:
        yield db          # la entrega al endpoint
    finally:
        db.close()   