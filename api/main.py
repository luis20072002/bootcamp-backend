from fastapi import FastAPI
from pydantic import BaseModel,Field
import hashlib
from datetime import date,time
from rutas.AulaMD import router as Aula_router
from rutas.UsuariosMD import router as Usuario_router

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
# # --- Docentes

# @app.post("/Docente")
# def add_docente(datos: Docente):
#     nuevo_docente={
#         "id" : Docente.id,
#         "nombre" : Docente.nombre,
#         "apellido" : Docente.apellido,
#         "correo" : Docente.correo,
#         "telefono" : Docente.telefono
#         }
#     docentes.append(nuevo_docente)

# @app.get("/Docente/{id}")
# def get_docente_by_id(id: int):
#      for docente in docentes:
#         if docente["id"] == id:
#             return docente

#         return {"error": "usuario no encontrado"}


# @app.put("/docente/{id}")
# def update_email(id: int, email: str):

#     for docente in docentes:
#         if docente["id"] == id:
#             docente["email"] = email
#             return {"mensaje": "email actualizado", "docente": docente}

#     return {"error": "docente no encontrado"}



# @app.delete("/Docente/{id}")
# def delete_docente_by_ID(id: int):
#       for i, registro in enumerate(docentes):
#         if registro["id"] == id:
#             usuarios.pop(i)
#             return {"mensaje": "Docente eliminado"}

#         return {"error": "Docente no encontrado"}
      

# # --- Cursos ---

# @app.post("/Cursos/")
# def crear_curso(datos: Curso):

#     docente_existe = False

#     for docente in docentes:
#         if docente["id"] == datos.id_docente:
#             docente_existe = True
#             break

#     if not docente_existe:
#         return {"error": "Docente no encontrado"}
    
#     curso = {
#         "id": len(cursos),
#         "nombre": datos.nombre,
#         "docente_id": datos.id_docente

#     }

#     cursos.append(curso)

#     return {"Mensaje": "Curso registrado con exito"}

# @app.get("/Cursos/{id}")
# def get_Curso_by_id(id: int):

#     for curso in cursos:
#         if curso["id"] == id:
#             return curso

#     return {"error": "Curso no encontrado"}

# @app.put("/Cursos/{id}")
# def actualizar_docente(id:int, docente_id: int):

#     for curso in cursos:
#         if curso["id"] == id:
#             curso["docente_id"] = docente_id
#             return {"mensaje": "docente actualizado", "curso": curso}

#     return {"error": "curso no encontrado"}


# @app.delete("/curso/{id}")
# def eliminar_curso(id: int):

#     for i, curso in enumerate(cursos):
#         if curso["id"] == id:
#             cursos.pop(i)
#             return {"mensaje": "curso eliminado"}

#     return {"error": "curso no encontrado"}


# # --- TURNOS ---
# @app.post("/turnos")
# def crear_turno(datos: Turno):

#     turno = {
#         "id": datos.id,
#         "fecha": datos.fecha,
#         "hora_inicio": datos.hora_inicio,
#         "hora_fin": datos.hora_fin
#     }

#     turnos.append(turno)

#     return {"mensaje": "turno creado", "turno": turno}


# @app.get("/turnos")
# def get_turnos():
#     return turnos


# @app.get("/turnos/{id}")
# def get_turno_by_id(id: int):

#     for turno in turnos:
#         if turno["id"] == id:
#             return turno

#     return {"error": "turno no encontrado"}


# @app.put("/turnos/{id}")
# def actualizar_turno(id: int, datos: Turno):

#     for turno in turnos:
#         if turno["id"] == id:
#             turno["fecha"] = datos.fecha
#             turno["hora_inicio"] = datos.hora_inicio
#             turno["hora_fin"] = datos.hora_fin

#             return {"mensaje": "turno actualizado", "turno": turno}

#     return {"error": "turno no encontrado"}

# @app.delete("/turnos/{id}")
# def eliminar_turno(id: int):

#     for i, turno in enumerate(turnos):
#         if turno["id"] == id:
#             turnos.pop(i)
#             return {"mensaje": "turno eliminado"}

#     return {"error": "turno no encontrado"}