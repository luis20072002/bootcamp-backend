from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from model.Aula import Aula
from schemas.Aula_SCH import AulaCreate, AulaResponse

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("/", response_model=list[AulaResponse])
def get_aulas(db: Session = Depends(get_db)):
    return db.query(Aula).all()


@router.get("/{id_aula}", response_model=AulaResponse)
def get_aula(id_aula: str, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.post("/", response_model=AulaResponse, status_code=201)
def crear_aula(datos: AulaCreate, db: Session = Depends(get_db)):
    existe = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if existe:
        raise HTTPException(status_code=400, detail="El id de aula ya existe")

    nueva_aula = Aula(
        id_aula=datos.id_aula,
        nombre_aula=datos.nombre_aula,
        edificio=datos.edificio,
        capacidad=datos.capacidad,
    )
    db.add(nueva_aula)
    db.commit()
    db.refresh(nueva_aula)
    return nueva_aula


@router.put("/{id_aula}", response_model=AulaResponse)
def actualizar_aula(id_aula: str, datos: AulaCreate, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    aula.nombre_aula = datos.nombre_aula
    aula.edificio = datos.edificio
    aula.capacidad = datos.capacidad

    db.commit()
    db.refresh(aula)
    return aula


@router.delete("/{id_aula}", status_code=200)
def eliminar_aula(id_aula: str, db: Session = Depends(get_db)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    db.delete(aula)
    db.commit()
    return {"detail": "Aula eliminada"}