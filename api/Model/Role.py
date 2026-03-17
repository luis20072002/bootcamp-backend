from pydantic import BaseModel,Field

class Role(BaseModel):
    id=int
    nombre= str