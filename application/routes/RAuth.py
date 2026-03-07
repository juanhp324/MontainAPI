from fastapi import APIRouter
from application.schemas.VAuth import Login_Schema   
from application.services.SAuth import validate_and_login

router = APIRouter(prefix="/auth", tags=["Authentication"]) 

@router.post("/login") 
def login_endpoint(payload: Login_Schema): 
    return validate_and_login(payload)     