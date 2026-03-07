from fastapi import APIRouter, Depends
from application.core.security import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    return {
        "message": "Acceso concedido al área privada",
        "user": user 
    }