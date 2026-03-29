from .connection import users_col
from application.core.resilience import db_circuit

@db_circuit
def search_user_by_email(email: str):
    user = users_col.find_one({"email": email})
    
    if user:
        # Convertimos _id a id (string) para consistencia y seguridad
        user["id"] = str(user["_id"])
        if "_id" in user:
            del user["_id"]
        return user
    
    return None