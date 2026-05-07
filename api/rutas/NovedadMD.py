from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date

from ..database.database import get_db
from ..model.Novedad import Novedad
from ..model.Registro import Registro
from ..model.Aula import Aula
from ..model.Usuario import Usuario
from ..schemas.Novedad_SCH import NovedadCreate, NovedadResponse, NovedadDetalleResponse
from ..auth.dependencies import solo_admin, solo_auxiliar, admin_o_auxiliar, ROL_AUXILIAR
from api.model.Edificio import Edificio


router = APIRouter(prefix="/novedades", tags=["Novedades"])


@router.get("/mis-novedades", response_model=list[NovedadResponse])
def get_mis_novedades(
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    query = (
        db.query(Novedad)
        .join(Registro, Registro.id_registro == Novedad.id_registro)
        .filter(Registro.id_usuario == current_user.id_usuario)
    )
    if fecha_inicio is not None:
        query = query.filter(Novedad.fecha_novedad >= datetime.combine(fecha_inicio, datetime.min.time()))
    if fecha_fin is not None:
        query = query.filter(Novedad.fecha_novedad <= datetime.combine(fecha_fin, datetime.max.time()))
    return query.all()


@router.get("/", response_model=list[NovedadResponse])
def get_novedades(
    id_edificio: int | None = Query(None),
    id_aula: int | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    query = db.query(Novedad)
    if id_aula is not None or id_edificio is not None:
        query = query.join(Registro, Registro.id_registro == Novedad.id_registro)
        if id_aula is not None:
            query = query.filter(Registro.id_aula == id_aula)
        if id_edificio is not None:
            query = query.join(Aula, Aula.id_aula == Registro.id_aula).filter(Aula.id_edificio == id_edificio)
    if fecha_inicio is not None:
        query = query.filter(Novedad.fecha_novedad >= datetime.combine(fecha_inicio, datetime.min.time()))
    if fecha_fin is not None:
        query = query.filter(Novedad.fecha_novedad <= datetime.combine(fecha_fin, datetime.max.time()))
    return query.all()

@router.get("/detalle", response_model=list[NovedadDetalleResponse])
def get_novedades_detalle(
    id_edificio:  int | None = Query(None),
    id_aula:      int | None = Query(None),
    id_usuario:   int | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin:    date | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin),
):
    """
    Devuelve todas las novedades con JOIN completo:
    aula, edificio y auxiliar que reportó.
    Análogo a GET /registros/detalle.
    """
    query = (
        db.query(
            Novedad.id_novedad,
            Novedad.id_registro,
            Novedad.descripcion,
            Novedad.fecha_novedad,
            # Aula (via registro)
            Aula.id_aula,
            Aula.codigo.label("aula_codigo"),
            Aula.nombre_aula.label("aula_nombre"),
            Aula.piso,
            # Edificio (via aula)
            Edificio.id_edificio,
            Edificio.nombre.label("nombre_edificio"),
            # Auxiliar
            Usuario.id_usuario,
            Usuario.nombre.label("auxiliar_nombre"),
        )
        .join(Registro, Registro.id_registro == Novedad.id_registro)
        .join(Aula,     Aula.id_aula         == Registro.id_aula)
        .join(Edificio, Edificio.id_edificio == Aula.id_edificio)
        .join(Usuario,  Usuario.id_usuario   == Registro.id_usuario)
    )
 
    if id_edificio:  query = query.filter(Edificio.id_edificio == id_edificio)
    if id_aula:      query = query.filter(Aula.id_aula         == id_aula)
    if id_usuario:   query = query.filter(Usuario.id_usuario   == id_usuario)
    if fecha_inicio: query = query.filter(Novedad.fecha_novedad >= fecha_inicio)
    if fecha_fin:    query = query.filter(Novedad.fecha_novedad <= fecha_fin)
 
    rows = query.all()
    return [row._asdict() for row in rows]
 

@router.get("/{id_novedad}", response_model=NovedadResponse)
def get_novedad(
    id_novedad: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    novedad = db.query(Novedad).filter(Novedad.id_novedad == id_novedad).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada")

    if current_user.rol_id == ROL_AUXILIAR:
        registro = db.query(Registro).filter(Registro.id_registro == novedad.id_registro).first()
        if not registro or registro.id_usuario != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="Solo puedes ver tus propias novedades")

    return novedad


@router.post("/", response_model=NovedadResponse, status_code=201)
def crear_novedad(
    datos: NovedadCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)
):
    registro = db.query(Registro).filter(Registro.id_registro == datos.id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if registro.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=403,
            detail="Solo puedes agregar novedades a tus propios registros"
        )

    nueva = Novedad(
        id_registro=datos.id_registro,
        descripcion=datos.descripcion,
        fecha_novedad=datetime.now(),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
