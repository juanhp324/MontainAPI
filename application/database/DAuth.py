from .connection import users_col

def search_user_by_email(email: str):
    user = users_col.find_one({"email": email})
    
    if user:
        user["_id"] = str(user["_id"])
        return user
    
    return None