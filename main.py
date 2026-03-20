from fastapi import FastAPI
from api.rutas.UsuariosMD import router

app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router)

