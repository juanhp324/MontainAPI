from fastapi import HTTPException      
from application.database.DAuth import search_user_by_email
from application.core.security import create_access_token
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def validate_and_login(user_data):
    user = search_user_by_email(user_data.email)
    
    if not user or hash_password(user_data.password) != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_access_token({"sub": user["email"]})
    return {"message": "Inicio exitoso", "token": token}