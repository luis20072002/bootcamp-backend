from pydantic import BaseModel

class RolCreate(BaseModel):

    nombre_rol : str

class RolResponse(BaseModel):
    rol_id : int

