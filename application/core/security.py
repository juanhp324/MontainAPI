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

def create_access_token(data: dict):
    data_to_encrypt = data.copy()
    
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=60)
    
    data_to_encrypt.update({"exp": expiration_time})
    
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
    return payload