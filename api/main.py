from fastapi import FastAPI
from api.rutas.RolMD import router as router_Roles
from api.rutas.UsuariosMD import router as router_Usuarios
import api.model as model

print("Roles router prefix:", router_Roles.prefix)  # 👈
print("Usuarios router prefix:", router_Usuarios.prefix)  # 👈

app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router_Usuarios)
app.include_router(router_Roles)