from fastapi import FastAPI
import model as model

from rutas.RolMD import router as router_Roles
from rutas.UsuariosMD import router as router_Usuarios
from rutas.AulaMD import router as router_Aulas
from rutas.DocentesMD import router as router_Docentes
from rutas.TurnosMD import router as router_Turnos
from rutas.CursosMD import router as router_Cursos
from rutas.HorarioMD import router as router_Horarios
from rutas.PlanillasMD import router as router_Planillas
from rutas.RegistroMD import router as router_Registros

app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router_Roles)
app.include_router(router_Usuarios)
app.include_router(router_Aulas)
app.include_router(router_Docentes)
app.include_router(router_Turnos)
app.include_router(router_Cursos)
app.include_router(router_Horarios)
app.include_router(router_Planillas)
app.include_router(router_Registros)