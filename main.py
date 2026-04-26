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
from api.rutas.authMD import router as router_Auth
from api.rutas.EdificioMD import router as router_Edificios
from api.rutas.HorarioClaseMD import router as router_HorariosClase
from api.rutas.NovedadMD import router as router_Novedades
from api.rutas.SolicitudMD import router as router_Solicitudes
from api.rutas.HistorialMD import router as router_Historial
import api.model as model
from api.database.database import Base,engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SGS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
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
app.include_router(router_Edificios)
app.include_router(router_HorariosClase)
app.include_router(router_Novedades)
app.include_router(router_Solicitudes)
app.include_router(router_Historial)
