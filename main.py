from fastapi import FastAPI
from api.rutas.UsuariosMD import router as router_Usuarios

app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router_Usuarios)

