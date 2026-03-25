from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from  api.database.database import get_db
from  api.model.Planilla import Planilla
from  api.model.Usuario import Usuario
from  api.model.Turno import Turno
from  api.schemas.Planilla_SCH import PlanillaCreate, PlanillaResponse

router = APIRouter(prefix="/planillas", tags=["Planillas"])


@router.get("/", response_model=list[PlanillaResponse])
def get_planillas(db: Session = Depends(get_db)):
    return db.query(Planilla).all()


@router.get("/{id_planilla}", response_model=PlanillaResponse)
def get_planilla(id_planilla: int, db: Session = Depends(get_db)):
    planilla = db.query(Planilla).filter(Planilla.id_planilla == id_planilla).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    return planilla


@router.get("/usuario/{id_usuario}", response_model=list[PlanillaResponse])
def get_planillas_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Planilla).filter(Planilla.id_usuario == id_usuario).all()


@router.post("/", response_model=PlanillaResponse, status_code=201)
def crear_planilla(datos: PlanillaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    turno = db.query(Turno).filter(Turno.id_turno == datos.id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    nueva_planilla = Planilla(
        id_usuario=datos.id_usuario,
        id_turno=datos.id_turno,
        fecha_asignacion=datetime.combine(datos.fecha_asignacion, datetime.min.time()),
    )
    db.add(nueva_planilla)
    db.commit()
    db.refresh(nueva_planilla)
    return nueva_planilla


@router.delete("/{id_planilla}", status_code=200)
def eliminar_planilla(id_planilla: int, db: Session = Depends(get_db)):
    planilla = db.query(Planilla).filter(Planilla.id_planilla == id_planilla).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    db.delete(planilla)
    db.commit()
    return {"detail": "Planilla eliminada"}