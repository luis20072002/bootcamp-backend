import models, schemas
from sqlalchemy.orm import Session

# CREATE
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# READ
def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()


# READ BY ID
def obtener_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


# DELETE
def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    
    if usuario:
        db.delete(usuario)
        db.commit()

    return usuario