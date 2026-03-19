from pydantic import BaseModel,Field
from enum import Enum

class RoleEnum(int, Enum):
    ADMIN = 1
    USUARIO = 0
class Role(BaseModel):
    id: RoleEnum
    nombre: str