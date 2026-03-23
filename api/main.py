from fastapi import FastAPI
from rutas.UsuariosMD import router
import model  # esto carga todos los modelos en el orden correcto

app = FastAPI(title="SGS API", version="1.0.0")
app.include_router(router)