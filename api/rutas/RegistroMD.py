from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.model.Registro import Registro
from api.model.Turno import Turno
from api.model.Aula import Aula
from api.model.Docente import Docente
from api.model.Curso import Curso
from api.model.Usuario import Usuario
from api.schemas.Registro_SCH import RegistroCreate, RegistroResponse

from api.auth.dependencies import solo_admin, solo_auxiliar, admin_o_auxiliar

router = APIRouter(prefix="/registros", tags=["Registros"])


@router.get("/", response_model=list[RegistroResponse])
def crear_registro(
    datos: RegistroCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_auxiliar)   # solo auxiliar registra
):
    return db.query(Registro).all()


@router.get("/{id_registro}", response_model=RegistroResponse)
def get_registro(id_registro: int, db: Session = Depends(get_db), current_user: Usuario = Depends(solo_admin)):
    registro = db.query(Registro).filter(Registro.id_registro == id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro


@router.get("/turno/{id_turno}", response_model=list[RegistroResponse])
def get_registros_por_turno(id_turno: int, db: Session = Depends(get_db),current_user: Usuario = Depends(admin_o_auxiliar)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return db.query(Registro).filter(Registro.id_turno == id_turno).all()


@router.post("/", response_model=RegistroResponse, status_code=201)
def crear_registro(datos: RegistroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(solo_auxiliar)):
    # Validar dependencias
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

    nuevo_registro = Registro(
        id_turno=datos.id_turno,
        id_aula=datos.id_aula,
        id_docente=datos.id_docente,
        id_curso=datos.id_curso,
        asistencia_docente=datos.asistencia,
        uso_medios_audiovisuales=datos.uso_medio_solicitudes,
        solicitudes=datos.solicitudes,
        novedades=datos.novedades,
        fecha_registro=datos.fecha_registro,
        hora_registro=datos.hora_registro,
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro


@router.delete("/{id_registro}", status_code=200)
def eliminar_registro(id_registro: int, db: Session = Depends(get_db), current_user: Usuario = Depends(admin_o_auxiliar)):
    registro = db.query(Registro).filter(Registro.id_registro == id_registro).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(registro)
    db.commit()
    return {"detail": "Registro eliminado"}