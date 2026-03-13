from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios")
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = models.Usuario(nombre=usuario.nombre, email=usuario.email)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo