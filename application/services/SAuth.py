from fastapi import HTTPException      
from application.database.DAuth import search_user_by_email
from application.core.security import create_access_token, create_refresh_token, check_token
import bcrypt


def validate_and_login(user_data):
    user = search_user_by_email(user_data.email)
    
    # Verificación segura con bcrypt
    if not user or not bcrypt.checkpw(user_data.password.encode(), user["password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    payload = {
        "sub": user["email"],
        "role": user.get("role", "user")
    }
    
    # Generamos ambos tokens
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    
    return {
        "message": "Inicio exitoso", 
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def refresh_access_token(token: str):
    payload = check_token(token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token de refresco inválido")
    
    # Generamos nuevo access token
    new_payload = {
        "sub": payload["sub"],
        "role": payload.get("role", "user")
    }
    return {"access_token": create_access_token(new_payload)}