from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext # instala passlib[bcrypt]
from datetime import datetime


from api.database.database import get_db
from api.model.Usuario import Usuario
from api.schemas.Usuario_SCH import UsuarioCreate, UsuarioResponse , UsuarioUpdate
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Configuración del hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@router.get("/", response_model=list[UsuarioResponse])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{id}", response_model=UsuarioResponse)
def get_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el nombre ya existe
    existe = db.query(Usuario).filter(Usuario.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    # Hashear la contraseña antes de guardar
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        pwsd=hashear_password(datos.pwsd),  # nunca se guarda en texto plano
        estado=datos.estado,
        rol_id=datos.rol_id,
        fecha_creacion=datetime.now(),
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
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

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}", status_code=200)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"detail": "Usuario eliminado"}