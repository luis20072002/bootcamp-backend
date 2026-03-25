from fastapi import FastAPI
from api.rutas.RolMD import router as router_Roles
from api.rutas.UsuariosMD import router as router_Usuarios
from api.rutas.AulaMD import router as router_aulas
from api.rutas.DocentesMD import router as router_docentes
from api.rutas.CursosMD import router as router_cursos
from api.rutas.HorarioMD import router as router_horario
from api.rutas.TurnosMD import router as router_turnos
from api.rutas.RegistroMD import router as router_registro
from api.rutas.PlanillasMD import router as router_planillas


import api.model as model

print("Roles router prefix:", router_Roles.prefix)  # 👈
print("Usuarios router prefix:", router_Usuarios.prefix)  # 👈

app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router_Usuarios)
app.include_router(router_Roles)
app.include_router(router_docentes)
app.include_router(router_cursos)
app.include_router(router_horario)
app.include_router(router_turnos)
app.include_router(router_registro)
app.include_router(router_planillas)
app.include_router(router_aulas)