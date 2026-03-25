from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from model.Role import Rol
from schemas.Rol_SCH import RolCreate, RolResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RolResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()


@router.get("/{id}", response_model=RolResponse)
def get_rol(id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.rol_id == id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.post("/", response_model=RolResponse, status_code=201)
def crear_rol(datos: RolCreate, db: Session = Depends(get_db)):
    existe = db.query(Rol).filter(Rol.nombre_rol == datos.nombre_rol).first()
    if existe:
        raise HTTPException(status_code=400, detail="El rol ya existe")

    nuevo_rol = Rol(nombre_rol=datos.nombre_rol)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol


@router.delete("/{id}", status_code=200)
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.rol_id == id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    return {"detail": "Rol eliminado"}