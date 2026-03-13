from fastapi import FastAPI

app=FastAPI()

salon=[]
#obtiene el salon
@app.get("/salon")
def obtenerSalon():
    return salon
#crear usuario
@app.post ("/salon")
def subirSalon(nombre:str):
    salon.append(nombre)
    return {"Mensaje":"Salon creado", "Salon: ":salon}
#actualizar
@app.put ("/salon/{id}")
def actualizarSalon(id: int, nombre:str):
    salon[id]=nombre
    return {"mensaje":"Salon actualizado", "Salon": salon}
#borarr
@app.delete("/salon{id}/")
def eliminarSalon(id: int, nombre:str):
    salon.pop(id)
    return {"mensaje": "Salon borrado", "Salon": salon}