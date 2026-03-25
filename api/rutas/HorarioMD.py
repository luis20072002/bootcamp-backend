from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from model.Horario import Horario
from model.Usuario import Usuario
from schemas.Horario_SCH import HorarioCreate, HorarioResponse

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/", response_model=list[HorarioResponse])
def get_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()


@router.get("/{id_horario}", response_model=HorarioResponse)
def get_horario(id_horario: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@router.get("/usuario/{id_usuario}", response_model=list[HorarioResponse])
def get_horarios_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Horario).filter(Horario.id_usuario == id_usuario).all()


@router.post("/", response_model=HorarioResponse, status_code=201)
def crear_horario(datos: HorarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_horario = Horario(
        id_usuario=datos.id_usuario,
        dia_semana=datos.dia_semana,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
    )
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return nuevo_horario


@router.put("/{id_horario}", response_model=HorarioResponse)
def actualizar_horario(id_horario: int, datos: HorarioCreate, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    horario.id_usuario = datos.id_usuario
    horario.dia_semana = datos.dia_semana
    horario.hora_inicio = datos.hora_inicio
    horario.hora_fin = datos.hora_fin

    db.commit()
    db.refresh(horario)
    return horario


@router.delete("/{id_horario}", status_code=200)
def eliminar_horario(id_horario: int, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()
    return {"detail": "Horario eliminado"}