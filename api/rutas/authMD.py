from fastapi import APIRouter, HTTPException
from api.core.security import create_access_token
from api.database.database import get_db

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(username: str, password: str):
    db=get_db()
    user = db.query(Usuario).filter(Usuario.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": user.id})

    return {"access_token": token, "token_type": "bearer"}