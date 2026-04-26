from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.Model.Aula import Aula
from api.Model.Edificio import Edificio
from api.Model.Registro import Registro
from api.schemas.Aula_SCH import AulaCreate, AulaResponse
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("/", response_model=list[AulaResponse])
def get_aulas(db: Session = Depends(get_db), current_user=Depends(admin_o_auxiliar)):
    return db.query(Aula).all()


@router.get("/edificio/{id_edificio}", response_model=list[AulaResponse])
def get_aulas_por_edificio(
    id_edificio: int,
    piso: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(admin_o_auxiliar)
):
    edificio = db.query(Edificio).filter(Edificio.id_edificio == id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    query = db.query(Aula).filter(Aula.id_edificio == id_edificio)
    if piso is not None:
        query = query.filter(Aula.piso == piso)
    return query.all()


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
    edificio = db.query(Edificio).filter(Edificio.id_edificio == datos.id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    if datos.piso < 1 or datos.piso > edificio.cantidad_pisos:
        raise HTTPException(
            status_code=400,
            detail=f"El piso debe estar entre 1 y {edificio.cantidad_pisos}"
        )

    existe = db.query(Aula).filter(Aula.codigo == datos.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El codigo de aula ya existe")

    nueva_aula = Aula(
        codigo=datos.codigo,
        nombre_aula=datos.nombre_aula if datos.nombre_aula else datos.codigo,
        piso=datos.piso,
        capacidad=datos.capacidad,
        id_edificio=datos.id_edificio,
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

    edificio = db.query(Edificio).filter(Edificio.id_edificio == datos.id_edificio).first()
    if not edificio:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")

    if datos.piso < 1 or datos.piso > edificio.cantidad_pisos:
        raise HTTPException(
            status_code=400,
            detail=f"El piso debe estar entre 1 y {edificio.cantidad_pisos}"
        )

    codigo_existe = db.query(Aula).filter(
        Aula.codigo == datos.codigo,
        Aula.id_aula != id_aula
    ).first()
    if codigo_existe:
        raise HTTPException(status_code=400, detail="El codigo ya está en uso")

    aula.codigo = datos.codigo
    aula.nombre_aula = datos.nombre_aula if datos.nombre_aula else datos.codigo
    aula.piso = datos.piso
    aula.capacidad = datos.capacidad
    aula.id_edificio = datos.id_edificio

    db.commit()
    db.refresh(aula)
    return aula


@router.delete("/{id_aula}", status_code=200)
def eliminar_aula(id_aula: int, db: Session = Depends(get_db), current_user=Depends(solo_admin)):
    aula = db.query(Aula).filter(Aula.id_aula == id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    tiene_registros = db.query(Registro).filter(Registro.id_aula == id_aula).first()
    if tiene_registros:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el aula: tiene registros asociados"
        )

    db.delete(aula)
    db.commit()
    return {"detail": "Aula eliminada"}
