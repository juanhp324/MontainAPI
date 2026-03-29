import pytest
import bcrypt
from application.core.security import create_access_token, check_token, create_refresh_token

def test_password_hashing():
    password = "password123"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    assert bcrypt.checkpw(password.encode(), hashed.encode('utf-8'))
    assert not bcrypt.checkpw("wrongpass".encode(), hashed.encode('utf-8'))

def test_jwt_tokens():
    payload = {"sub": "test@example.com", "role": "admin"}
    
    # Test Access Token
    access_token = create_access_token(payload)
    decoded_access = check_token(access_token)
    assert decoded_access["sub"] == "test@example.com"
    assert decoded_access["role"] == "admin"
    assert decoded_access["type"] == "access"
    
    # Test Refresh Token
    refresh_token = create_refresh_token(payload)
    decoded_refresh = check_token(refresh_token)
    assert decoded_refresh["type"] == "refresh"

if __name__ == "__main__":
    test_password_hashing()
    test_jwt_tokens()
    print("✅ Pruebas de lógica básica pasadas con éxito")
