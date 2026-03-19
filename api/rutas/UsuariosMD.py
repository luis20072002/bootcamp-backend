from fastapi import APIRouter
from model.Usuario import Usuario, UsuarioUpdate
import hashlib
from datetime import datetime

usuarios: list[dict] = [] #check

router = APIRouter(
    prefix="/usuario",
    tags=["Usuario"]
)

@router.post("/usuario")
def crear_usuario(datos: Usuario):

    hash_pwsd = hashlib.sha256(datos.pwsd.encode()).hexdigest()

    usuario = {
        "id": len(usuarios),
        "nombre": datos.nombre,
        "password": hash_pwsd,
        "rol": datos.rol_id,
        "fecha_creacion": datetime.now(),
    }

    usuarios.append(usuario)

    return {"mensaje": "usuario creado", "usuario": usuario}


@router.get("/usuario/{id}")
def get_usuario_by_id(id: int):

    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    return {"error": "usuario no encontrado"}


@router.put("/usuarios/{nombre}")
def actualizar_nombre(nombre: str, datos: UsuarioUpdate):

    for usuario in usuarios:
        if usuario["nombre"] == nombre:
            usuario["nombre"] = datos.nuevo_nombre
            return {"mensaje": "usuario actualizado", "usuario": usuario}

    return {"error": "usuario no encontrado"}


@router.delete("/usuario/{id}")
def delete_user_by_ID(id: int):
    for i, registro in enumerate(usuarios):
        if registro["id"] == id:
            usuarios.pop(i)
            return {"mensaje": "Usuario eliminado"}

    return {"error": "Usuario no encontrado"}