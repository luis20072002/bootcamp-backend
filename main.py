from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.rutas.RolMD import router as router_Roles
from api.rutas.UsuariosMD import router as router_Usuarios
from api.rutas.AulaMD import router as router_Aulas
from api.rutas.DocentesMD import router as router_Docentes
from api.rutas.TurnosMD import router as router_Turnos
from api.rutas.CursosMD import router as router_Cursos
from api.rutas.HorarioMD import router as router_Horarios
from api.rutas.PlanillasMD import router as router_Planillas
from api.rutas.RegistroMD import router as router_Registros
from api.rutas.AuthMD import router as router_Auth
import api.model as model

app = FastAPI(title="SGS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # en producción cambia esto por la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_Auth)
app.include_router(router_Roles)
app.include_router(router_Usuarios)
app.include_router(router_Aulas)
app.include_router(router_Docentes)
app.include_router(router_Turnos)
app.include_router(router_Cursos)
app.include_router(router_Horarios)
app.include_router(router_Planillas)
app.include_router(router_Registros)