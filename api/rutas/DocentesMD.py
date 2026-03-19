from fastapi import APIRouter
from model.Docente import Docente

docentes: list[dict] = [] #check

router=APIRouter(
    prefix="/Docente",
    tags=["Docente"]
)
#Deberia aparecer el telefono? no, Cambio para la base de datos
# --- Docentes

@router.post("/Docente")
def add_docente(datos: Docente):
    nuevo_docente={
        "id" : Docente.id,
        "nombre" : Docente.nombre,
        "apellido" : Docente.apellido,
        "correo" : Docente.correo,
        }
    docentes.append(nuevo_docente)

@router.get("/Docente/{id}")
def get_docente_by_id(id: int):
    for docente in docentes:
        if docente["id"] == id:
            return docente

    return {"error": "usuario no encontrado"}
@router.put("/Docente/{id}")
def update_docente_by_id (id:int, datos:Docente):
    for Docente in docentes:
        if Docente["id"]==id:
            Docente["nombre"]= datos.nombre
            Docente["apellido"]= datos.apellido
            Docente["correo"]=datos.correo

            return {"Mensaje: Docente actualizado"}
    return {"error":"Docente not found"}

@router.put("/Docente/{id}")
def update_email(id: int, email: str):

    for docente in docentes:
        if docente["id"] == id:
            docente["email"] = email
            return {"mensaje": "email actualizado", "docente": docente}

    return {"error": "docente no encontrado"}

@router.delete("/Docente/{id}")
def delete_docente_by_ID(id: int):
      for i, registro in enumerate(docentes):
        if registro["id"] == id:
            docentes.pop(i)
            return {"mensaje": "Docente eliminado"}

        return {"error": "Docente no encontrado"}

