from fastapi import APIRouter, HTTPException
from api.core.security import create_access_token
from api.database.database import get_db

router = APIRouter(prefix="/auth")

@router.post("/login")
def login():