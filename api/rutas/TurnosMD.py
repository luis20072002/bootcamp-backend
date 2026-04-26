from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.Model.Turno import Turno
from api.Model.Planilla import Planilla
from api.Model.Usuario import Usuario
from api.schemas.Turno_SCH import TurnoCreate, TurnoResponse, TurnoUpdate
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=list[TurnoResponse])
def get_turnos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    return db.query(Turno).all()


@router.get("/{id_turno}", response_model=TurnoResponse)
def get_turno(
    id_turno: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return turno


@router.post("/", response_model=TurnoResponse, status_code=201)
def crear_turno(
    datos: TurnoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    if datos.hora_fin <= datos.hora_inicio:
        raise HTTPException(status_code=400, detail="hora_fin debe ser mayor que hora_inicio")

    nuevo_turno = Turno(
        nombre_turno=datos.nombre_turno,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


@router.put("/{id_turno}", response_model=TurnoResponse)
def actualizar_turno(
    id_turno: int,
    datos: TurnoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    if datos.nombre_turno is not None:
        turno.nombre_turno = datos.nombre_turno
    if datos.hora_inicio is not None:
        turno.hora_inicio = datos.hora_inicio
    if datos.hora_fin is not None:
        turno.hora_fin = datos.hora_fin

    if turno.hora_fin <= turno.hora_inicio:
        raise HTTPException(status_code=400, detail="hora_fin debe ser mayor que hora_inicio")

    db.commit()
    db.refresh(turno)
    return turno


@router.delete("/{id_turno}", status_code=200)
def eliminar_turno(
    id_turno: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    planillas_activas = db.query(Planilla).filter(
        Planilla.id_turno == id_turno,
        Planilla.estado == 'activa'
    ).first()
    if planillas_activas:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el turno: tiene planillas activas asociadas"
        )

    db.delete(turno)
    db.commit()
    return {"detail": "Turno eliminado"}
