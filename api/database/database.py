from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pyodbc

from dotenv import load_dotenv
import os
load_dotenv()
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()  # abre la sesión
    try:
        yield db          # la entrega al endpoint
    finally:
        db.close()   
