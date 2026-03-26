from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.model.Curso import Curso
from api.model.Docente import Docente
from api.model.Aula import Aula
from api.model.Usuario import Usuario
from api.schemas.Curso_SCH import CursoCreate, CursoResponse
from api.auth.dependencies import solo_admin, admin_o_auxiliar

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=list[CursoResponse])
def get_cursos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    return db.query(Curso).all()


@router.get("/{id_curso}", response_model=CursoResponse)
def get_curso(
    id_curso: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_o_auxiliar)
):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.post("/", response_model=CursoResponse, status_code=201)
def crear_curso(
    datos: CursoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    existe = db.query(Curso).filter(Curso.id_curso == datos.id_curso).first()
    if existe:
        raise HTTPException(status_code=400, detail="El id de curso ya existe")

    nuevo_curso = Curso(
        id_curso=datos.id_curso,
        nombre_curso=datos.nombre_curso,
        codi_curso=datos.codi_curso,
        id_docente=datos.id_docente,
        id_aula=datos.id_aula,
    )
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    return nuevo_curso


@router.put("/{id_curso}", response_model=CursoResponse)
def actualizar_curso(
    id_curso: str,
    datos: CursoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    docente = db.query(Docente).filter(Docente.id_docente == datos.id_docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    aula = db.query(Aula).filter(Aula.id_aula == datos.id_aula).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    curso.nombre_curso = datos.nombre_curso
    curso.codi_curso = datos.codi_curso
    curso.id_docente = datos.id_docente
    curso.id_aula = datos.id_aula

    db.commit()
    db.refresh(curso)
    return curso


@router.delete("/{id_curso}", status_code=200)
def eliminar_curso(
    id_curso: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    curso = db.query(Curso).filter(Curso.id_curso == id_curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(curso)
    db.commit()
    return {"detail": "Curso eliminado"}