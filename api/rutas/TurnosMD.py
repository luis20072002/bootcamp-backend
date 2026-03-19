from fastapi import APIRouter
from model.Turno import Turno

turnos: list[dict] = [] 

router=APIRouter(
    prefix="/Turno",
    tags=["Turnos"]
)

# --- TURNOS ---
@router.post("")
def crear_turno(datos: Turno):

    turno = {
        "id": datos.id,
        "fecha": datos.fecha,
        "hora_inicio": datos.hora_inicio,
        "hora_fin": datos.hora_fin
    }

    turnos.append(turno)

    return {"mensaje": "turno creado", "turno": turno}


@router.get("")
def get_turnos():
    return turnos


@router.get("/{id}")
def get_turno_by_id(id: int):

    for turno in turnos:
        if turno["id"] == id:
            return turno

    return {"error": "turno no encontrado"}


@router.put("/{id}")
def actualizar_turno(id: int, datos: Turno):

    for turno in turnos:
        if turno["id"] == id:
            turno["fecha"] = datos.fecha
            turno["hora_inicio"] = datos.hora_inicio
            turno["hora_fin"] = datos.hora_fin

            return {"mensaje": "turno actualizado", "turno": turno}

    return {"error": "turno no encontrado"}

@router.delete("/{id}")
def eliminar_turno(id: int):

    for i, turno in enumerate(turnos):
        if turno["id"] == id:
            turnos.pop(i)
            return {"mensaje": "turno eliminado"}

    return {"error": "turno no encontrado"}