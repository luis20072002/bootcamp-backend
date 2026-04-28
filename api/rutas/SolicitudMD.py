from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date

from ..database.database import get_db
from ..model.Solicitud import Solicitud
from ..model.Registro import Registro
from ..model.Aula import Aula
from ..model.Usuario import Usuario
from ..schemas.Solicitud_SCH import SolicitudCreate, SolicitudResponse, SolicitudUpdateEstado
from ..auth.dependencies import (
    solo_admin,
    solo_auxiliar,
    admin_o_auxiliar,
    get_current_user,
    ROL_ADMIN,
    ROL_AUXILIAR,
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.get("/mis-solicitudes", response_model=list[SolicitudResponse])
def get_mis_solicitudes(
    estado: str | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    query = (
        db.query(Solicitud)
        .join(Registro, Registro.id_registro == Solicitud.id_registro)
        .filter(Registro.id_usuario == current_user.id_usuario)
    )
    if estado is not None:
        query = query.filter(Solicitud.estado == estado)
    if fecha_inicio is not None:
        query = query.filter(Solicitud.fecha_solicitud >= datetime.combine(fecha_inicio, datetime.min.time()))
    if fecha_fin is not None:
        query = query.filter(Solicitud.fecha_solicitud <= datetime.combine(fecha_fin, datetime.max.time()))
    return query.all()


@router.get("/", response_model=list[SolicitudResponse])
def get_solicitudes(
    estado: str | None = Query(None),
    id_edificio: int | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    query = db.query(Solicitud)
    if estado is not None:
        query = query.filter(Solicitud.estado == estado)
    if id_edificio is not None:
        query = (
            query.join(Registro, Registro.id_registro == Solicitud.id_registro)
            .join(Aula, Aula.id_aula == Registro.id_aula)
            .filter(Aula.id_edificio == id_edificio)
        )
    if fecha_inicio is not None:
        query = query.filter(Solicitud.fecha_solicitud >= datetime.combine(fecha_inicio, datetime.min.time()))
    if fecha_fin is not None:
        query = query.filter(Solicitud.fecha_solicitud <= datetime.combine(fecha_fin, datetime.max.time()))
    return query.all()


@router.get("/{id_solicitud}", response_model=SolicitudResponse)
def get_solicitud(
    id_solicitud: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    solicitud = db.query(Solicitud).filter(Solicitud.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if current_user.rol_id == ROL_AUXILIAR:
        registro = db.query(Registro).filter(Registro.id_registro == solicitud.id_registro).first()
        if not registro or registro.id_usuario != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="Solo puedes ver tus propias solicitudes")

    return solicitud


@router.post("/", response_model=SolicitudResponse, status_code=201)
def crear_solicitud(
    datos: SolicitudCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    registro = db.query(Registro).filter(Registro.id_registro == datos.id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if registro.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=403,
            detail="Solo puedes agregar solicitudes a tus propios registros"
        )

    nueva = Solicitud(
        id_registro=datos.id_registro,
        descripcion=datos.descripcion,
        estado='pendiente',
        fecha_solicitud=datetime.now(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.patch("/{id_solicitud}/estado", response_model=SolicitudResponse)
def cambiar_estado_solicitud(
    id_solicitud: int,
    datos: SolicitudUpdateEstado,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol_id not in (ROL_ADMIN, ROL_AUXILIAR):
        raise HTTPException(status_code=403, detail="Acceso denegado")

    solicitud = db.query(Solicitud).filter(Solicitud.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if solicitud.estado == 'resuelta':
        raise HTTPException(
            status_code=400,
            detail="Una solicitud resuelta no puede cambiar de estado"
        )

    if current_user.rol_id == ROL_AUXILIAR:
        registro = db.query(Registro).filter(Registro.id_registro == solicitud.id_registro).first()
        if not registro or registro.id_usuario != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="Solo puedes modificar tus propias solicitudes")

        if datos.estado != 'resuelta':
            raise HTTPException(
                status_code=403,
                detail="Como auxiliar solo puedes marcar la solicitud como 'resuelta'"
            )
        if not datos.nota_resolucion:
            raise HTTPException(
                status_code=400,
                detail="nota_resolucion es obligatoria al resolver una solicitud"
            )

        solicitud.estado = 'resuelta'
        solicitud.nota_resolucion = datos.nota_resolucion
        solicitud.resuelta_por_auxiliar = True
        solicitud.fecha_resolucion = datetime.now()

    else:
        if datos.estado not in ('en_proceso', 'resuelta'):
            raise HTTPException(
                status_code=400,
                detail="estado debe ser 'en_proceso' o 'resuelta'"
            )
        solicitud.estado = datos.estado
        if datos.nota_resolucion is not None:
            solicitud.nota_resolucion = datos.nota_resolucion
        if datos.estado == 'resuelta':
            solicitud.resuelta_por_auxiliar = False
            solicitud.fecha_resolucion = datetime.now()

    db.commit()
    db.refresh(solicitud)
    return solicitud
