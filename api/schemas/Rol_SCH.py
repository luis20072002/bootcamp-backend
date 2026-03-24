from pydantic import BaseModel

class RolCreate(BaseModel):

    nombre_rol : str

class RolResponse(BaseModel):
    rol_id : int
    nombre_rol: str

    model_config = {
        "from_attributes": True
    }
