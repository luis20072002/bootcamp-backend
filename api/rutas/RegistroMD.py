from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date

from api.database.database import get_db
from api.model.Registro import Registro
from api.model.Turno import Turno
from api.model.Aula import Aula
from api.model.Docente import Docente
from api.model.Curso import Curso
from api.model.Usuario import Usuario
from api.model.Planilla import Planilla
from api.schemas.Registro_SCH import RegistroCreate, RegistroResponse

from api.auth.dependencies import solo_admin, solo_auxiliar, admin_o_auxiliar, ROL_AUXILIAR, ROL_ADMIN

router = APIRouter(prefix="/registros", tags=["Registros"])


@router.get("/mis-registros", response_model=list[RegistroResponse])
def get_mis_registros(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    return db.query(Registro).filter(Registro.id_usuario == current_user.id_usuario).all()


@router.get("/", response_model=list[RegistroResponse])
def get_registros(
    id_edificio: int | None = Query(None),
    id_aula: int | None = Query(None),
    id_docente: int | None = Query(None),
    id_turno: int | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    query = db.query(Registro)
    if id_aula is not None:
        query = query.filter(Registro.id_aula == id_aula)
    if id_docente is not None:
        query = query.filter(Registro.id_docente == id_docente)
    if id_turno is not None:
        query = query.filter(Registro.id_turno == id_turno)
    if fecha_inicio is not None:
        query = query.filter(Registro.fecha_registro >= fecha_inicio)
    if fecha_fin is not None:
        query = query.filter(Registro.fecha_registro <= fecha_fin)
    if id_edificio is not None:
        query = query.join(Aula, Aula.id_aula == Registro.id_aula).filter(Aula.id_edificio == id_edificio)
    return query.all()


@router.get("/{id_registro}", response_model=RegistroResponse)
def get_registro(
    id_registro: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    registro = db.query(Registro).filter(Registro.id_registro == id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if current_user.rol_id == ROL_AUXILIAR and registro.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes ver tus propios registros")

    return registro


@router.post("/", response_model=RegistroResponse, status_code=201)
def crear_registro(
    datos: RegistroCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    turno = db.query(Turno).filter(Turno.id_turno == datos.id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    curso = db.query(Curso).filter(Curso.id_curso == datos.id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    planilla_activa = db.query(Planilla).filter(
        Planilla.id_usuario == current_user.id_usuario,
        Planilla.id_turno == datos.id_turno,
        Planilla.estado == 'activa',
    ).first()
    if not planilla_activa:
        raise HTTPException(
            status_code=403,
            detail="No tienes una planilla activa para este turno"
        )

    hora_actual = datetime.now().time()
    if not (turno.hora_inicio <= hora_actual <= turno.hora_fin):
        raise HTTPException(
            status_code=403,
            detail="La hora actual no está dentro del lapso del turno"
        )

    nuevo_registro = Registro(
        id_turno=datos.id_turno,
        id_aula=datos.id_aula,
        id_docente=datos.id_docente,
        id_curso=datos.id_curso,
        id_usuario=current_user.id_usuario,
        asistencia_docente=datos.asistencia_docente,
        uso_medios_audiovisuales=datos.uso_medios_audiovisuales,
        fecha_registro=datos.fecha_registro,
        hora_registro=datos.hora_registro,
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro


@router.put("/{id_registro}", response_model=RegistroResponse)
def actualizar_registro(
    id_registro: int,
    datos: RegistroCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    registro = db.query(Registro).filter(Registro.id_registro == id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if registro.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="Solo puedes editar tus propios registros")

    turno = db.query(Turno).filter(Turno.id_turno == registro.id_turno).first()
    hora_actual = datetime.now().time()
    if hora_actual > turno.hora_fin:
        raise HTTPException(
            status_code=403,
            detail="El turno ya finalizó, no se puede editar este registro"
        )

    aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    curso = db.query(Curso).filter(Curso.id_curso == datos.id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    registro.id_aula = datos.id_aula
    registro.id_docente = datos.id_docente
    registro.id_curso = datos.id_curso
    registro.asistencia_docente = datos.asistencia_docente
    registro.uso_medios_audiovisuales = datos.uso_medios_audiovisuales
    registro.fecha_registro = datos.fecha_registro
    registro.hora_registro = datos.hora_registro

    db.commit()
    db.refresh(registro)
    return registro


@router.delete("/{id_registro}", status_code=200)
def eliminar_registro(
    id_registro: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    registro = db.query(Registro).filter(Registro.id_registro == id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(registro)
    db.commit()
    return {"detail": "Registro eliminado"}
