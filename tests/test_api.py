import pytest
import bcrypt

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "API Montain funcionando"

def test_login_flow(client, setup_mock_db):
    email = "user@test.com"
    password = "secure_password"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    # Insertar usuario en mock db
    setup_mock_db["users"].insert_one({
        "email": email,
        "password": hashed,
        "role": "user"
    })
    
    # Intentar login
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_create_booking_authenticated(client, auth_headers):
    # Datos de reserva
    payload = {
        "date": "2026-12-31",
        "type": "sleep",
        "names_sleepers": [{"name": "Juan"}],
        "include_food": True
    }
    
    response = client.post("/booking/create", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert "Reserva procesada exitosamente" in response.json()["message"]

def test_create_booking_unauthenticated(client):
    payload = {
        "date": "2026-12-31",
        "type": "pass_day",
        "names_sleepers": [{"name": "Anonimo"}],
    }
    response = client.post("/booking/create", json=payload)
    assert response.status_code == 401  # Requiere login

def test_admin_access_denied_for_regular_user(client, setup_mock_db):
    # Crear usuario normal
    from application.core.security import create_access_token
    token = create_access_token({"sub": "regular@test.com", "role": "user", "type": "access"})
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/booking/admin/manage/all", headers=headers)
    assert response.status_code == 403  # Acceso denegado
