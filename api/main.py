from fastapi import FastAPI
from rutas.UsuariosMD import router
from model import Usuario, Role, Aula, Curso, Docente, Horario, Planilla, Turno, Registro
app = FastAPI(title="SGS API", version="1.0.0")

app.include_router(router)