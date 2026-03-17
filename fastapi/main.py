from fastapi import FastAPI
from pydantic import BaseModel,Field
import hashlib
from datetime import date,time

# NOTA: SEPARAR MODELOS A OTRO ARCHIVO DIFERENTE AL MAIN
# SOLO DEBERIAN HABER ENDPOINTS EN ESTE ARCHIVO

app = FastAPI()

# --- MODELOS ---

class Aula(BaseModel):
    codigo: str = Field(pattern=r"^A[1-5]-[1-6](0[1-9]|1[0-9]|20)$")
    nombre: str | None = None
    edificio: str
    capacidad: int
    
class Usuario(BaseModel):
    nombre: str
    pwsd: str
    admin: bool = False


class UsuarioUpdate(BaseModel):
    nuevo_nombre: str

class Docente(BaseModel):
    id : int
    nombre : str
    apellido : str
    correo : str
    telefono: str

class Curso(BaseModel):
    id : int
    nombre : str
    codigo : str
    id_docente : int
    

class Turno(BaseModel):
    id : int
    fecha : date
    hora_inicio : time
    hora_fin : time
    estado_turno : bool


# --- BASES DE DATOS SIMULADAS ---

aula: list[dict] = [] #check
usuarios: list[dict] = [] #check

cursos: list[dict] = [] # check
Horarios_trabajo: list[dict] = []
turnos: list[dict] = [] 
Planilla_trabajo: list[dict] = []
docentes: list[dict] = [] #check 
Registros_aula: list[dict] = []


# --- AULA ---

@app.post("/aula")
def subiraula(datos: Aula):

    for registro in aula:
        if registro["codigo"] == datos.codigo:
            return {"error": "el codigo ya existe"}

    nueva_aula = {
        "id": len(aula),
        "codigo": datos.codigo,
        "nombre": datos.nombre if datos.nombre else datos.codigo,
        "edificio": datos.edificio,
        "capacidad": datos.capacidad
    }

    aula.append(nueva_aula)

    return {"mensaje": "aula creada", "aula": nueva_aula}


@app.get("/aula/{id}")
def get_aula_by_id(id: int):

    for registro in aula:
        if registro["id"] == id:
            return registro

    return {"error": "aula no encontrada"}


@app.put("/aula/{id}")
def actualizaraula(id: int, datos: Aula):

    for registro in aula:
        if registro["id"] == id:
            registro["codigo"] = datos.codigo
            registro["nombre"] = datos.nombre if datos.nombre else datos.codigo
            registro["edificio"] = datos.edificio
            registro["capacidad"] = datos.capacidad

            return {"mensaje": "aula actualizada", "aula": registro}

    return {"error": "aula no encontrada"}
#endpoint para buscar por aula:
@app.get("/aula/codigo/{codigo}")
def get_aula_by_codigo(codigo: str):

    for registro in aula:
        if registro["codigo"] == codigo:
            return registro

    return {"error": "aula no encontrada"}
@app.delete("/aula/{id}")
def eliminaraula(id: int):

    for i, registro in enumerate(aula):
        if registro["id"] == id:
            aula.pop(i)
            return {"mensaje": "aula eliminada con id: " + str(id)}

    return {"error": "aula no encontrada"}



# --- USUARIOS ---

@app.post("/usuario")
def crear_usuario(datos: Usuario):

    hash_pwsd = hashlib.sha256(datos.pwsd.encode()).hexdigest()

    usuario = {
        "id": len(usuarios),
        "nombre": datos.nombre,
        "password": hash_pwsd,
        "rol": "administrador" if datos.admin else "auxiliar"
    }

    usuarios.append(usuario)

    return {"mensaje": "usuario creado", "usuario": usuario}


@app.get("/usuario/{id}")
def get_usuario_by_id(id: int):

    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    return {"error": "usuario no encontrado"}


@app.put("/usuarios/{nombre}")
def actualizar_nombre(nombre: str, datos: UsuarioUpdate):

    for usuario in usuarios:
        if usuario["nombre"] == nombre:
            usuario["nombre"] = datos.nuevo_nombre
            return {"mensaje": "usuario actualizado", "usuario": usuario}

    return {"error": "usuario no encontrado"}


@app.delete("/usuario/{id}")
def delete_user_by_ID(id: int):
      for i, registro in enumerate(usuarios):
        if registro["id"] == id:
            usuarios.pop(i)
            return {"mensaje": "Usuario eliminado"}

        return {"error": "Usuario no encontrado"}
      
# --- Docentes

@app.post("/Docente")
def add_docente(datos: Docente):
    nuevo_docente={
        "id" : Docente.id,
        "nombre" : Docente.nombre,
        "apellido" : Docente.apellido,
        "correo" : Docente.correo,
        "telefono" : Docente.telefono
        }
    docentes.append(nuevo_docente)

@app.get("/Docente/{id}")
def get_docente_by_id(id: int):
     for docente in docentes:
        if docente["id"] == id:
            return docente

        return {"error": "usuario no encontrado"}


@app.put("/docente/{id}")
def update_email(id: int, email: str):

    for docente in docentes:
        if docente["id"] == id:
            docente["email"] = email
            return {"mensaje": "email actualizado", "docente": docente}

    return {"error": "docente no encontrado"}



@app.delete("/Docente/{id}")
def delete_docente_by_ID(id: int):
      for i, registro in enumerate(docentes):
        if registro["id"] == id:
            usuarios.pop(i)
            return {"mensaje": "Docente eliminado"}

        return {"error": "Docente no encontrado"}
      

#--- Cursos ---

@app.post("/Cursos/")
def crear_curso(datos: Curso):

    docente_existe = False

    for docente in docentes:
        if docente["id"] == datos.id_docente:
            docente_existe = True
            break

    if not docente_existe:
        return {"error": "Docente no encontrado"}
    
    curso = {
        "id": len(cursos),
        "nombre": datos.nombre,
        "docente_id": datos.id_docente

    }

    cursos.append(curso)

    return {"Mensaje": "Curso registrado con exito"}

@app.get("/Cursos/{id}")
def get_Curso_by_id(id: int):

    for curso in cursos:
        if curso["id"] == id:
            return curso

    return {"error": "Curso no encontrado"}

@app.put("/Cursos/{id}")
def actualizar_docente(id:int, docente_id: int):

    for curso in cursos:
        if curso["id"] == id:
            curso["docente_id"] = docente_id
            return {"mensaje": "docente actualizado", "curso": curso}

    return {"error": "curso no encontrado"}


@app.delete("/curso/{id}")
def eliminar_curso(id: int):

    for i, curso in enumerate(cursos):
        if curso["id"] == id:
            cursos.pop(i)
            return {"mensaje": "curso eliminado"}

    return {"error": "curso no encontrado"}


#--- TURNOS ---
@app.post("/turnos")
def crear_turno(datos: Turno):

    turno = {
        "id": datos.id,
        "fecha": datos.fecha,
        "hora_inicio": datos.hora_inicio,
        "hora_fin": datos.hora_fin
    }

    turnos.append(turno)

    return {"mensaje": "turno creado", "turno": turno}


@app.get("/turnos")
def get_turnos():
    return turnos


@app.get("/turnos/{id}")
def get_turno_by_id(id: int):

    for turno in turnos:
        if turno["id"] == id:
            return turno

    return {"error": "turno no encontrado"}


@app.put("/turnos/{id}")
def actualizar_turno(id: int, datos: Turno):

    for turno in turnos:
        if turno["id"] == id:
            turno["fecha"] = datos.fecha
            turno["hora_inicio"] = datos.hora_inicio
            turno["hora_fin"] = datos.hora_fin

            return {"mensaje": "turno actualizado", "turno": turno}

    return {"error": "turno no encontrado"}

@app.delete("/turnos/{id}")
def eliminar_turno(id: int):

    for i, turno in enumerate(turnos):
        if turno["id"] == id:
            turnos.pop(i)
            return {"mensaje": "turno eliminado"}

    return {"error": "turno no encontrado"}