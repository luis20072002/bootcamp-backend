from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.Model.Usuario import Usuario
from api.auth.auth import verificar_token

from typing import Optional
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

ROL_ADMIN    = 1
ROL_AUXILIAR = 2

# Modo desarrollo
DEBUG = False


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:

    #  BYPASS
    if DEBUG:
        return Usuario(
            id_usuario=1,
            nombre="admin",
            correo="admin@test.com",
            rol_id=ROL_ADMIN,
            estado=True
        )

    #  Lógica original
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == int(payload.get("sub"))
    ).first()

    if not usuario or not usuario.estado:
        raise HTTPException(
            status_code=401,
            detail="Usuario inactivo o no encontrado"
        )

    return usuario


def solo_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.rol_id != ROL_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Solo el administrador puede hacer esto"
        )
    return current_user


def solo_auxiliar(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.rol_id != ROL_AUXILIAR:
        raise HTTPException(
            status_code=403,
            detail="Solo el auxiliar puede hacer esto"
        )
    return current_user


def admin_o_auxiliar(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.rol_id not in (ROL_ADMIN, ROL_AUXILIAR):
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado"
        )
    return current_user