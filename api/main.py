from fastapi import FastAPI
from pydantic import BaseModel,Field
import hashlib
from datetime import date,time
from rutas.AulaMD import router as Aula_router
from rutas.UsuariosMD import router as Usuario_router
from rutas.DocentesMD import router as Docente_router
from rutas.TurnosMD import router as Turnos_router
# NOTA: SEPARAR MODELOS A OTRO ARCHIVO DIFERENTE AL MAIN
# SOLO DEBERIAN HABER ENDPOINTS EN ESTE ARCHIVO

app = FastAPI()


# cursos: list[dict] = [] # check
# Horarios_trabajo: list[dict] = []
# turnos: list[dict] = [] 
# Planilla_trabajo: list[dict] = []
# docentes: list[dict] = [] #check 
# Registros_aula: list[dict] = []

app.include_router(Aula_router)
app.include_router(Usuario_router)
app.include_router(Docente_router)
app.include_router(Turnos_router)
