from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

from api.database.database import get_db
from api.model.Usuario import Usuario
from api.rutas.UsuariosMD import verificar_password
from api.auth.auth import crear_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.correo == form.username).first()

    if not usuario or not verificar_password(form.password, usuario.pwsd):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    usuario.ultima_actividad = datetime.now()
    db.commit()

    token = crear_token({"sub": str(usuario.id_usuario), "rol": usuario.rol_id})
    return {"access_token": token, "token_type": "bearer"}
