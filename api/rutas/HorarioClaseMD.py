from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from api.database.database import get_db
from api.model.HorarioClase import HorarioClase
from api.model.Planilla import Planilla
from api.model.Aula import Aula
from api.model.Docente import Docente
from api.model.Curso import Curso
from api.model.Turno import Turno
from api.model.Usuario import Usuario
from api.schemas.HorarioClase_SCH import (HorarioClaseCreate,HorarioClaseResponse,HorarioClaseUpdate)
from api.auth.dependencies import solo_admin, admin_o_auxiliar


router = APIRouter(prefix="/horarios-clase", tags=["HorariosClase"])


def _validar_dentro_turno(db: Session, id_planilla: int, hora_inicio, hora_fin):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planilla).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    turno = db.query(Turno).filter(Turno.id_turno == planilla.id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno de la planilla no encontrado")

    if hora_inicio < turno.hora_inicio or hora_fin > turno.hora_fin:
        raise HTTPException(
            status_code=400,
            detail="Las horas de la clase deben estar dentro del rango del turno de la planilla"
        )
    if hora_fin <= hora_inicio:
        raise HTTPException(status_code=400, detail="hora_fin debe ser mayor que hora_inicio")
    return planilla


@router.get("/planilla/{id_planilla}", response_model=list[HorarioClaseResponse])
def get_clases_por_planilla(
    id_planilla: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    planilla = db.query(Planilla).filter(Planilla.id_planillas == id_planilla).first()
    if not planilla:
        raise HTTPException(status_code=404, detail="Planilla no encontrada")
    return db.query(HorarioClase).filter(HorarioClase.id_planilla == id_planilla).all()


@router.get("/{id_horario_clase}", response_model=HorarioClaseResponse)
def get_horario_clase(
    id_horario_clase: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    clase = db.query(HorarioClase).filter(HorarioClase.id_horario_clase == id_horario_clase).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Horario de clase no encontrado")
    return clase


@router.post("/", response_model=HorarioClaseResponse, status_code=201)
def crear_horario_clase(
    datos: HorarioClaseCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    _validar_dentro_turno(db, datos.id_planilla, datos.hora_inicio, datos.hora_fin)

    aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    curso = db.query(Curso).filter(Curso.id_curso == datos.id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    nueva = HorarioClase(
        id_planilla=datos.id_planilla,
        id_aula=datos.id_aula,
        id_docente=datos.id_docente,
        id_curso=datos.id_curso,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        dia_semana=datos.dia_semana,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{id_horario_clase}", response_model=HorarioClaseResponse)
def actualizar_horario_clase(
    id_horario_clase: int,
    datos: HorarioClaseUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    clase = db.query(HorarioClase).filter(HorarioClase.id_horario_clase == id_horario_clase).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Horario de clase no encontrado")

    nueva_hi = datos.hora_inicio if datos.hora_inicio is not None else clase.hora_inicio
    nueva_hf = datos.hora_fin if datos.hora_fin is not None else clase.hora_fin
    if datos.hora_inicio is not None or datos.hora_fin is not None:
        _validar_dentro_turno(db, clase.id_planilla, nueva_hi, nueva_hf)

    if datos.id_aula is not None:
        aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
        if not aula:
            raise HTTPException(status_code=404, detail="Aula no encontrada")
        clase.id_aula = datos.id_aula

    if datos.id_docente is not None:
        docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
        if not docente:
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        clase.id_docente = datos.id_docente

    if datos.id_curso is not None:
        curso = db.query(Curso).filter(Curso.id_curso == datos.id_curso).first()
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        clase.id_curso = datos.id_curso

    if datos.hora_inicio is not None:
        clase.hora_inicio = datos.hora_inicio
    if datos.hora_fin is not None:
        clase.hora_fin = datos.hora_fin
    if datos.dia_semana is not None:
        clase.dia_semana = datos.dia_semana

    db.commit()
    db.refresh(clase)
    return clase


@router.delete("/{id_horario_clase}", status_code=200)
def eliminar_horario_clase(
    id_horario_clase: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    clase = db.query(HorarioClase).filter(HorarioClase.id_horario_clase == id_horario_clase).first()
    if not clase:
        raise HTTPException(status_code=404, detail="Horario de clase no encontrado")
    db.delete(clase)
    db.commit()
    return {"detail": "Horario de clase eliminado"}
