from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.model.Edificio import Edificio
from api.model.Aula import Aula
from api.model.Usuario import Usuario
from api.schemas.Edificio_SCH import EdificioCreate, EdificioResponse, EdificioUpdate
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/edificios", tags=["Edificios"])


@router.get("/", response_model=list[EdificioResponse])
def get_edificios(db: Session = Depends(get_db), current_user: Usuario = Depends(admin_o_auxiliar)):
    return db.query(Edificio).all()


@router.get("/{id_edificio}", response_model=EdificioResponse)
def get_edificio(
    id_edificio: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    edificio = db.query(Edificio).filter(Edificio.id_edificio == id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    return edificio


@router.post("/", response_model=EdificioResponse, status_code=201)
def crear_edificio(
    datos: EdificioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    existe = db.query(Edificio).filter(Edificio.codigo == datos.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El codigo de edificio ya existe")

    nuevo = Edificio(
        nombre=datos.nombre,
        codigo=datos.codigo,
        cantidad_pisos=datos.cantidad_pisos,
        estado=True,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id_edificio}", response_model=EdificioResponse)
def actualizar_edificio(
    id_edificio: int,
    datos: EdificioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    edificio = db.query(Edificio).filter(Edificio.id_edificio == id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    if datos.codigo is not None and datos.codigo != edificio.codigo:
        codigo_existe = db.query(Edificio).filter(
            Edificio.codigo == datos.codigo,
            Edificio.id_edificio != id_edificio
        ).first()
        if codigo_existe:
            raise HTTPException(status_code=400, detail="El codigo ya está en uso")
        edificio.codigo = datos.codigo

    if datos.nombre is not None:
        edificio.nombre = datos.nombre
    if datos.cantidad_pisos is not None:
        edificio.cantidad_pisos = datos.cantidad_pisos
    if datos.estado is not None:
        edificio.estado = datos.estado

    db.commit()
    db.refresh(edificio)
    return edificio


@router.delete("/{id_edificio}", status_code=200)
def eliminar_edificio(
    id_edificio: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    edificio = db.query(Edificio).filter(Edificio.id_edificio == id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    tiene_aulas = db.query(Aula).filter(Aula.id_edificio == id_edificio).first()
    tiene_usuarios = db.query(Usuario).filter(Usuario.id_edificio == id_edificio).first()

    if tiene_aulas or tiene_usuarios:
        edificio.estado = False
        db.commit()
        return {"detail": "Edificio desactivado (tiene dependencias)"}

    db.delete(edificio)
    db.commit()
    return {"detail": "Edificio eliminado"}
