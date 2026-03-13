from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# URL de conexión
DATABASE_URL = "mssql+pyodbc://talento:cartagena@nodossolutions.com:1435/SGS?driver=ODBC+Driver+17+for+SQL+Server"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Crear sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()