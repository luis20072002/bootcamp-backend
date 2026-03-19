from fastapi import APIRouter
from model.Curso import CursoCreate
from rutas.DocentesMD import docentes
from rutas.AulaMD import aulas

router = APIRouter(
    prefix="/Curso",
    tags=["Curso"]
)
cursos: list[dict] = [] # check

# --- Curso ---

@router.post("/")
def crear_curso(datos: CursoCreate):

    # Validar docente
    if not any(docente["id"] == datos.id_docente for docente in docentes):
        return {"error": "Docente no encontrado"}

    # Validar aula
    if not any(aula["codigo"] == datos.codigo for aula in aulas):
        return {"error": "Aula no encontrada"}

    curso = {
        "id": len(cursos),
        "nombre": datos.nombre,
        "codigo": datos.codigo,
        "docente_id": datos.id_docente,
        "estatus": datos.estatus
    }

    cursos.append(curso)

    return {"mensaje": "Curso registrado con éxito", "curso": curso}
@router.get("/{id}")
def get_Curso_by_id(id: int):

    for curso in cursos:
        if curso["id"] == id:
            return curso

    return {"error": "Curso no encontrado"}

@router.put("/{id}")
def actualizar_docente_curso(id: int, docente_id: int):

    if not any(docente["id"] == docente_id for docente in docentes):
        return {"error": "Docente no encontrado"}

    for curso in cursos:
        if curso["id"] == id:
            curso["docente_id"] = docente_id
            return {"mensaje": "docente actualizado", "curso": curso}

    return {"error": "curso no encontrado"}

@router.delete("/{id}")
def eliminar_curso(id: int):

    for i, curso in enumerate(cursos):
        if curso["id"] == id:
            cursos.pop(i)
            return {"mensaje": "curso eliminado"}

    return {"error": "curso no encontrado"}
