from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date, time

from api.database.database import get_db
from api.Model.Planilla import Planilla
from api.Model.Usuario import Usuario
from api.Model.Turno import Turno
from api.Model.Edificio import Edificio
from api.Model.Registro import Registro
from api.schemas.Planilla_SCH import PlanillaCreate, PlanillaResponse, PlanillaUpdate
from api.auth.dependencies import solo_admin, admin_o_auxiliar, ROL_AUXILIAR

router = APIRouter(prefix="/planillas", tags=["Planillas"])


def _validar_pisos(piso_1: int, piso_2: int | None, piso_3: int | None, edificio: Edificio):
    pisos = [p for p in (piso_1, piso_2, piso_3) if p is not None]
    if len(pisos) > 3:
        raise HTTPException(status_code=400, detail="Máximo 3 pisos por planilla")
    for p in pisos:
        if p < 1 or p > edificio.cantidad_pisos:
            raise HTTPException(
                status_code=400,
                detail=f"El piso {p} debe estar entre 1 y {edificio.cantidad_pisos}"
            )


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


@router.get("/activa/{id_usuario}", response_model=PlanillaResponse)
def get_planilla_activa(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    if current_user.rol_id == ROL_AUXILIAR and current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes ver tus propias planillas")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ahora = datetime.now()
    hora_actual = ahora.time()

    planillas = (
        db.query(Planilla)
        .join(Turno, Turno.id_turno == Planilla.id_turno)
        .filter(
            Planilla.id_usuario == id_usuario,
            Planilla.estado == 'activa',
            Turno.hora_inicio <= hora_actual,
            Turno.hora_fin >= hora_actual,
        )
        .first()
    )
    if not planillas:
        raise HTTPException(status_code=404, detail="No hay planilla activa en este momento")
    return planillas


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

    edificio = db.query(Edificio).filter(Edificio.id_edificio == datos.id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    _validar_pisos(datos.piso_1, datos.piso_2, datos.piso_3, edificio)

    duplicada = db.query(Planilla).filter(
        Planilla.id_usuario == datos.id_usuario,
        Planilla.id_turno == datos.id_turno,
        Planilla.periodo_vigencia == datos.periodo_vigencia,
        Planilla.estado == 'activa',
    ).first()
    if duplicada:
        raise HTTPException(
            status_code=400,
            detail="El auxiliar ya tiene una planilla activa para este turno y período"
        )

    nueva_planilla = Planilla(
        id_usuario=datos.id_usuario,
        id_turno=datos.id_turno,
        id_edificio=datos.id_edificio,
        piso_1=datos.piso_1,
        piso_2=datos.piso_2,
        piso_3=datos.piso_3,
        periodo_vigencia=datos.periodo_vigencia,
        estado='activa',
        fecha_asignacion=datetime.combine(datos.fecha_asignacion, datetime.min.time()),
    )
    db.add(nueva_planilla)
    db.commit()
    db.refresh(nueva_planilla)
    return nueva_planilla


@router.put("/{id_planillas}", response_model=PlanillaResponse)
def actualizar_planilla(
    id_planillas: int,
    datos: PlanillaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planillas).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")

    if datos.estado is not None:
        if datos.estado not in ('activa', 'inactiva'):
            raise HTTPException(status_code=400, detail="estado debe ser 'activa' o 'inactiva'")
        planilla.estado = datos.estado

    nuevo_piso_1 = datos.piso_1 if datos.piso_1 is not None else planilla.piso_1
    nuevo_piso_2 = datos.piso_2 if datos.piso_2 is not None else planilla.piso_2
    nuevo_piso_3 = datos.piso_3 if datos.piso_3 is not None else planilla.piso_3

    if any(p is not None for p in (datos.piso_1, datos.piso_2, datos.piso_3)):
        edificio = db.query(Edificio).filter(Edificio.id_edificio == planilla.id_edificio).first()
        _validar_pisos(nuevo_piso_1, nuevo_piso_2, nuevo_piso_3, edificio)
        planilla.piso_1 = nuevo_piso_1
        planilla.piso_2 = nuevo_piso_2
        planilla.piso_3 = nuevo_piso_3

    db.commit()
    db.refresh(planilla)
    return planilla


@router.patch("/{id_planillas}/estado", response_model=PlanillaResponse)
def cambiar_estado_planilla(
    id_planillas: int,
    datos: PlanillaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planillas).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")

    if datos.estado is None or datos.estado not in ('activa', 'inactiva'):
        raise HTTPException(status_code=400, detail="estado debe ser 'activa' o 'inactiva'")

    planilla.estado = datos.estado
    db.commit()
    db.refresh(planilla)
    return planilla


@router.delete("/{id_planillas}", status_code=200)
def eliminar_planilla(
    id_planillas: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planillas).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")

    tiene_registros = (
        db.query(Registro)
        .filter(Registro.id_turno == planilla.id_turno, Registro.id_usuario == planilla.id_usuario)
        .first()
    )
    if tiene_registros:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: la planilla tiene registros asociados. Desactívala en su lugar."
        )

    db.delete(planilla)
    db.commit()
    return {"detail": "Planilla eliminada"}
