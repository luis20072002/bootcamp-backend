from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from model.Turno import Turno
from model.Usuario import Usuario
from schemas.Turno_SCH import TurnoCreate, TurnoResponse, TurnoUpdate

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=list[TurnoResponse])
def get_turnos(db: Session = Depends(get_db)):
    return db.query(Turno).all()


@router.get("/{id_turno}", response_model=TurnoResponse)
def get_turno(id_turno: int, db: Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return turno


@router.get("/usuario/{id_usuario}", response_model=list[TurnoResponse])
def get_turnos_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Turno).filter(Turno.id_usuario == id_usuario).all()


@router.post("/", response_model=TurnoResponse, status_code=201)
def crear_turno(datos: TurnoCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_turno = Turno(
        id_usuario=datos.id_usuario,
        fecha_turno=datos.fecha,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        estado_turno=datos.estado_turno,
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


@router.patch("/{id_turno}", response_model=TurnoResponse)
def actualizar_estado_turno(id_turno: int, datos: TurnoUpdate, db: Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    turno.estado_turno = datos.estado_turno
    db.commit()
    db.refresh(turno)
    return turno


@router.delete("/{id_turno}", status_code=200)
def eliminar_turno(id_turno: int, db: Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    db.delete(turno)
    db.commit()
    return {"detail": "Turno eliminado"}