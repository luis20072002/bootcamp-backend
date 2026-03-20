
from fastapi import APIRouter
from model.Aula import Aula


aula: list[dict] = [] #check

router = APIRouter(
    prefix="/Aula",
    tags=["Aula"]
)

# --- AULA ---

@router.post("/aula")
def subiraula(datos: Aula):

    for registro in aula:
        if registro["codigo"] == datos.codigo:
            return {"error": "el codigo ya existe"}

    nueva_aula = {
        "id": len(aula),
        "codigo": datos.codigo,
        "nombre": datos.nombre if datos.nombre else datos.codigo,
        "edificio": datos.edificio,
        "capacidad": datos.capacidad
    }

    aula.append(nueva_aula)

    return {"mensaje": "aula creada", "aula": nueva_aula}


@router.get("/aula/{id}")
def get_aula_by_id(id: int):

    for registro in aula:
        if registro["id"] == id:
            return registro

    return {"error": "aula no encontrada"}


@router.put("/aula/{id}")
def actualizaraula(id: int, datos: Aula):

    for registro in aula:
        if registro["id"] == id:
            registro["codigo"] = datos.codigo
            registro["nombre"] = datos.nombre if datos.nombre else datos.codigo
            registro["edificio"] = datos.edificio
            registro["capacidad"] = datos.capacidad

            return {"mensaje": "aula actualizada", "aula": registro}

    return {"error": "aula no encontrada"}
#endpoint para buscar por aula:
@router.get("/aula/codigo/{codigo}")
def get_aula_by_codigo(codigo: str):

    for registro in aula:
        if registro["codigo"] == codigo:
            return registro

    return {"error": "aula no encontrada"}
@router.delete("/aula/{id}")
def eliminaraula(id: int):

    for i, registro in enumerate(aula):
        if registro["id"] == id:
            aula.pop(i)
            return {"mensaje": "aula eliminada con id: " + str(id)}

    return {"error": "aula no encontrada"}
