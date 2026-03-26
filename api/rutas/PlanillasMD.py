from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from api.database.database import get_db
from api.model.Planilla import Planilla
from api.model.Usuario import Usuario
from api.model.Turno import Turno
from api.schemas.Planilla_SCH import PlanillaCreate, PlanillaResponse
from api.auth.dependencies import solo_admin, admin_o_auxiliar, ROL_AUXILIAR

router = APIRouter(prefix="/planillas", tags=["Planillas"])


@router.get("/", response_model=list[PlanillaResponse])
def get_planillas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    return db.query(Planilla).all()


@router.get("/usuario/{id_usuario}", response_model=list[PlanillaResponse])
def get_planillas_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    if current_user.rol_id == ROL_AUXILIAR and current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes ver tus propias planillas")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return db.query(Planilla).filter(Planilla.id_usuario == id_usuario).all()


@router.get("/{id_planillas}", response_model=PlanillaResponse)
def get_planilla(
    id_planillas: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planillas).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    return planilla


@router.post("/", response_model=PlanillaResponse, status_code=201)
def crear_planilla(
    datos: PlanillaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
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


@router.delete("/{id_planillas}", status_code=200)
def eliminar_planilla(
    id_planillas: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planillas).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    db.delete(planilla)
    db.commit()
    return {"detail": "Planilla eliminada"}