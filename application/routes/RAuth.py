from fastapi import APIRouter, Request, Body
from application.schemas.VAuth import Login_Schema   
from application.services.SAuth import validate_and_login, refresh_access_token
from application.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"]) 

@router.post("/login") 
@limiter.limit("5/minute")
def login_endpoint(request: Request, payload: Login_Schema): 
    return validate_and_login(payload)     

@router.post("/refresh")
def refresh_endpoint(refresh_token: str = Body(..., embed=True)):
    return refresh_access_token(refresh_token)