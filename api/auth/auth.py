from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "4f9c2a7d8e1b3c6f0a5d9e7c2b1f8a6d3c4e5f7a9b0c1d2e3f4a5b6c7d8e9f0a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def crear_token(data: dict) -> str:
    payload = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})
    return jwt.encode(payload, SECRET_KEY)


def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY)
    except JWTError:
        return None