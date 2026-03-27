from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.model.Aula import Aula
from api.schemas.Aula_SCH import AulaCreate, AulaResponse
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("/", response_model=list[AulaResponse])
def get_aulas(db=Depends(get_db), current_user=Depends(admin_o_auxiliar)):
    return db.query(Aula).all()


@router.get("/codigo/{codigo}", response_model=AulaResponse)
def get_aula_por_codigo(codigo: str, db: Session = Depends(get_db), current_user=Depends(admin_o_auxiliar)):
    aula = db.query(Aula).filter(Aula.codigo == codigo.upper()).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.get("/{id_aula}", response_model=AulaResponse)
def get_aula(id_aula: int, db: Session = Depends(get_db), current_user=Depends(admin_o_auxiliar)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.post("/", response_model=AulaResponse, status_code=201)
def crear_aula(datos: AulaCreate, db: Session = Depends(get_db), current_user=Depends(solo_admin)):
    existe = db.query(Aula).filter(Aula.codigo == datos.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El codigo de aula ya existe")

    nueva_aula = Aula(
        codigo=datos.codigo,
        nombre=datos.nombre,
        edificio=datos.edificio,
        capacidad=datos.capacidad,
    )
    db.add(nueva_aula)
    db.commit()
    db.refresh(nueva_aula)
    return nueva_aula


@router.put("/{id_aula}", response_model=AulaResponse)
def actualizar_aula(id_aula: int, datos: AulaCreate, db: Session = Depends(get_db), current_user=Depends(solo_admin)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    codigo_existe = db.query(Aula).filter(
        Aula.codigo == datos.codigo,
        Aula.id_aula != id_aula
    ).first()
    if codigo_existe:
        raise HTTPException(status_code=400, detail="El codigo ya está en uso")

    aula.codigo = datos.codigo
    aula.nombre = datos.nombre
    aula.edificio = datos.edificio
    aula.capacidad = datos.capacidad

    db.commit()
    db.refresh(aula)
    return aula


@router.delete("/{id_aula}", status_code=200)
def eliminar_aula(id_aula: int, db: Session = Depends(get_db), current_user=Depends(solo_admin)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    db.delete(aula)
    db.commit()
    return {"detail": "Aula eliminada"}