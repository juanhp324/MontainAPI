import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("La variable de entorno SECRET_KEY no está definida")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    data_to_encrypt = data.copy()
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encrypt.update({"exp": expiration_time, "type": "access"})
    token_final = jwt.encode(data_to_encrypt, SECRET_KEY, algorithm=ALGORITHM)
    return token_final

def create_refresh_token(data: dict):
    data_to_encrypt = data.copy()
    expiration_time = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data_to_encrypt.update({"exp": expiration_time, "type": "refresh"})
    token_final = jwt.encode(data_to_encrypt, SECRET_KEY, algorithm=ALGORITHM)
    return token_final

def check_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = check_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Se requiere un token de acceso")
    return payload

def check_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: se requieren permisos de administrador")
    return user