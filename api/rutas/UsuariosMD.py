from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime


from api.database.database import get_db
from api.Model.Usuario import Usuario
from api.Model.HistorialEdificioAuxiliar import HistorialEdificioAuxiliar
from api.schemas.Usuario_SCH import UsuarioCreate, UsuarioResponse, UsuarioUpdate

from api.auth.dependencies import get_current_user, solo_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@router.get("/me", response_model=UsuarioResponse)
def get_mi_perfil(
    current_user: Usuario = Depends(get_current_user)
):
    return current_user


@router.get("/", response_model=list[UsuarioResponse])
def get_usuarios(db: Session = Depends(get_db), current_user: Usuario = Depends(solo_admin)):
    return db.query(Usuario).all()


@router.get("/{id}", response_model=UsuarioResponse)
def get_usuario(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(solo_admin)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(solo_admin)):
    existe = db.query(Usuario).filter(Usuario.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        pwsd=hashear_password(datos.pwsd),
        estado=datos.estado,
        rol_id=datos.rol_id,
        fecha_creacion=datetime.now(),
        ultima_actividad=datetime.now(),
        correo=datos.correo,
        id_edificio=datos.id_edificio,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(
    id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.nombre is not None:
        existe = db.query(Usuario).filter(
            Usuario.nombre == datos.nombre,
            Usuario.id_usuario != id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="El nombre ya existe")
        usuario.nombre = datos.nombre

    if datos.pwsd is not None:
        usuario.pwsd = hashear_password(datos.pwsd)

    if datos.estado is not None:
        usuario.estado = datos.estado

    if datos.rol_id is not None:
        usuario.rol_id = datos.rol_id

    if datos.id_edificio is not None and datos.id_edificio != usuario.id_edificio:
        historial = HistorialEdificioAuxiliar(
            id_usuario=id,
            id_edificio_anterior=usuario.id_edificio,
            id_edificio_nuevo=datos.id_edificio,
            fecha_cambio=datetime.now(),
            id_admin=current_user.id_usuario,
        )
        db.add(historial)
        usuario.id_edificio = datos.id_edificio

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}", status_code=200)
def eliminar_usuario(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(solo_admin)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.estado = False
    db.commit()
    return {"detail": "Usuario desactivado"}
