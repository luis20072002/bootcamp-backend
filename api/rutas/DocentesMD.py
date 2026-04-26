from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.model.Docente import Docente
from api.model.Usuario import Usuario
from api.schemas.Docente_SCH import DocenteCreate, DocenteResponse
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("/", response_model=list[DocenteResponse])
def get_docentes(
    activos: bool | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    query = db.query(Docente)
    if activos is True:
        query = query.filter(Docente.estado == True)
    return query.all()


@router.get("/{id_docente}", response_model=DocenteResponse)
def get_docente(
    id_docente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente


@router.post("/", response_model=DocenteResponse, status_code=201)
def crear_docente(
    datos: DocenteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    existe = db.query(Docente).filter(Docente.correo == datos.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_docente = Docente(
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        telefono=datos.telefono,
    )
    db.add(nuevo_docente)
    db.commit()
    db.refresh(nuevo_docente)
    return nuevo_docente


@router.put("/{id_docente}", response_model=DocenteResponse)
def actualizar_docente(
    id_docente: int,
    datos: DocenteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    correo_existe = db.query(Docente).filter(
        Docente.correo == datos.correo,
        Docente.id_docente != id_docente
    ).first()
    if correo_existe:
        raise HTTPException(status_code=400, detail="El correo ya está en uso")

    docente.nombre = datos.nombre
    docente.apellido = datos.apellido
    docente.correo = datos.correo
    docente.telefono = datos.telefono

    db.commit()
    db.refresh(docente)
    return docente


@router.patch("/{id_docente}/activar", response_model=DocenteResponse)
def activar_docente(
    id_docente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    docente.estado = True
    db.commit()
    db.refresh(docente)
    return docente


@router.delete("/{id_docente}", status_code=200)
def eliminar_docente(
    id_docente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    docente = db.query(Docente).filter(Docente.id_docente == id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    docente.estado = False
    db.commit()
    db.refresh(docente)
    return {"detail": "Docente desactivado"}
