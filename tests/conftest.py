import pytest
import mongomock
from unittest.mock import patch

# Mockeamos la base de datos ANTES de importar la aplicación
@pytest.fixture(autouse=True, scope="session")
def setup_mock_db():
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["MountainDB"]
    
    with patch("application.database.connection.client", mock_client), \
         patch("application.database.connection.db", mock_db), \
         patch("application.database.connection.users_col", mock_db["users"]), \
         patch("application.database.connection.bookings_col", mock_db["bookings"]):
        yield mock_db

@pytest.fixture
def client():
    """Cliente de pruebas para FastAPI."""
    from fastapi.testclient import TestClient
    from application.main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers(client, setup_mock_db):
    """Crea un usuario admin y devuelve los headers con token."""
    import bcrypt
    from application.core.security import create_access_token
    
    email = "test@admin.com"
    password = "password123"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    setup_mock_db["users"].insert_one({
        "email": email, 
        "password": hashed,
        "role": "admin"
    })
    
    token = create_access_token({"sub": email, "role": "admin", "type": "access"})
    return {"Authorization": f"Bearer {token}"}
