from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


from api.database.database import get_db
from api.model.HorarioAuxiliar import HorarioAuxiliar
from api.model.HorarioExcepcion import HorarioExcepcion
from api.model.Usuario import Usuario
from api.model.Turno import Turno
from api.model.Planilla import Planilla

from api.schemas.HorarioAuxiliar_SCH import (HorarioAuxiliarCreate,HorarioAuxiliarResponse,HorarioAuxiliarUpdate)
from api.schemas.HorarioExcepcion_SCH import (HorarioExcepcionCreate,HorarioExcepcionResponse)

from api.auth.dependencies import solo_admin, admin_o_auxiliar, ROL_AUXILIAR


router = APIRouter(prefix="/horarios", tags=["Horarios"])


def _validar_turnos_consecutivos(db: Session, id_turno_1: int, id_turno_2: int | None):
    turno_1 = db.query(Turno).filter(Turno.id_turno == id_turno_1).first()
    if not turno_1:
        raise HTTPException(status_code=404, detail="id_turno_1 no encontrado")

    if id_turno_2 is None:
        return

    turno_2 = db.query(Turno).filter(Turno.id_turno == id_turno_2).first()
    if not turno_2:
        raise HTTPException(status_code=404, detail="id_turno_2 no encontrado")

    if turno_2.hora_inicio != turno_1.hora_fin:
        raise HTTPException(
            status_code=400,
            detail="Los turnos deben ser consecutivos (Turno1+Turno2 o Turno2+Turno3)"
        )


@router.get("/", response_model=list[HorarioAuxiliarResponse])
def get_horarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    return db.query(HorarioAuxiliar).all()


@router.get("/usuario/{id_usuario}", response_model=list[HorarioAuxiliarResponse])
def get_horario_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    if current_user.rol_id == ROL_AUXILIAR and current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes ver tu propio horario")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return db.query(HorarioAuxiliar).filter(HorarioAuxiliar.id_usuario == id_usuario).all()


@router.post("/", response_model=HorarioAuxiliarResponse, status_code=201)
def crear_horario(
    datos: HorarioAuxiliarCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    duplicado = db.query(HorarioAuxiliar).filter(
        HorarioAuxiliar.id_usuario == datos.id_usuario,
        HorarioAuxiliar.dia_semana == datos.dia_semana,
        HorarioAuxiliar.periodo_vigencia == datos.periodo_vigencia,
    ).first()
    if duplicado:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un horario para este usuario, día y período"
        )

    _validar_turnos_consecutivos(db, datos.id_turno_1, datos.id_turno_2)

    nuevo = HorarioAuxiliar(
        id_usuario=datos.id_usuario,
        dia_semana=datos.dia_semana,
        id_turno_1=datos.id_turno_1,
        id_turno_2=datos.id_turno_2,
        periodo_vigencia=datos.periodo_vigencia,
    )
    db.add(nuevo)

    if usuario.id_edificio is not None:
        planilla = db.query(Planilla).filter(
            Planilla.id_usuario == datos.id_usuario,
            Planilla.id_edificio == usuario.id_edificio,
            Planilla.id_turno == datos.id_turno_1,
            Planilla.periodo_vigencia == datos.periodo_vigencia,
            Planilla.estado == 'activa',
        ).first()
        if not planilla:
            nueva_planilla = Planilla(
                id_usuario=datos.id_usuario,
                id_turno=datos.id_turno_1,
                id_edificio=usuario.id_edificio,
                piso_1=1,
                piso_2=None,
                piso_3=None,
                periodo_vigencia=datos.periodo_vigencia,
                estado='activa',
                fecha_asignacion=datetime.now(),
            )
            db.add(nueva_planilla)

    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id_horario}", response_model=HorarioAuxiliarResponse)
def actualizar_horario(
    id_horario: int,
    datos: HorarioAuxiliarUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    horario = db.query(HorarioAuxiliar).filter(HorarioAuxiliar.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    nuevo_t1 = datos.id_turno_1 if datos.id_turno_1 is not None else horario.id_turno_1
    nuevo_t2 = datos.id_turno_2 if datos.id_turno_2 is not None else horario.id_turno_2
    if datos.id_turno_1 is not None or datos.id_turno_2 is not None:
        _validar_turnos_consecutivos(db, nuevo_t1, nuevo_t2)

    if datos.dia_semana is not None:
        horario.dia_semana = datos.dia_semana
    if datos.id_turno_1 is not None:
        horario.id_turno_1 = datos.id_turno_1
    if datos.id_turno_2 is not None:
        horario.id_turno_2 = datos.id_turno_2
    if datos.periodo_vigencia is not None:
        horario.periodo_vigencia = datos.periodo_vigencia

    db.commit()
    db.refresh(horario)
    return horario


@router.delete("/{id_horario}", status_code=200)
def eliminar_horario(
    id_horario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    horario = db.query(HorarioAuxiliar).filter(HorarioAuxiliar.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()
    return {"detail": "Horario eliminado"}


@router.get("/excepciones/usuario/{id_usuario}", response_model=list[HorarioExcepcionResponse])
def get_excepciones_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    if current_user.rol_id == ROL_AUXILIAR and current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes ver tus propias excepciones")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return db.query(HorarioExcepcion).filter(HorarioExcepcion.id_usuario == id_usuario).all()


@router.post("/excepciones/", response_model=HorarioExcepcionResponse, status_code=201)
def crear_excepcion(
    datos: HorarioExcepcionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.tipo not in ('cambio_turno', 'ausencia_justificada'):
        raise HTTPException(
            status_code=400,
            detail="tipo debe ser 'cambio_turno' o 'ausencia_justificada'"
        )

    if datos.tipo == 'cambio_turno':
        if datos.id_turno_nuevo is None:
            raise HTTPException(
                status_code=400,
                detail="id_turno_nuevo es obligatorio para tipo 'cambio_turno'"
            )
        turno = db.query(Turno).filter(Turno.id_turno == datos.id_turno_nuevo).first()
        if not turno:
            raise HTTPException(status_code=404, detail="Turno nuevo no encontrado")

    nueva = HorarioExcepcion(
        id_usuario=datos.id_usuario,
        fecha=datos.fecha,
        tipo=datos.tipo,
        id_turno_nuevo=datos.id_turno_nuevo,
        motivo=datos.motivo,
        id_admin=current_user.id_usuario,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.delete("/excepciones/{id_excepcion}", status_code=200)
def eliminar_excepcion(
    id_excepcion: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    excepcion = db.query(HorarioExcepcion).filter(HorarioExcepcion.id_excepcion == id_excepcion).first()
    if not excepcion:
        raise HTTPException(status_code=404, detail="Excepción no encontrada")
    db.delete(excepcion)
    db.commit()
    return {"detail": "Excepción eliminada"}
