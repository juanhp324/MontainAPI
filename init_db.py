from application.database.connection import users_col

def create_initial_admin():
    admin_email = "admin@respawn.rd"
    
    # Verificamos si ya existe para no duplicarlo
    if not users_col.find_one({"email": admin_email}):
        users_col.insert_one({
            "email": admin_email,
            "password": "123", # En producción deberías usar hash (bcrypt)
            "nombre": "Administrador Respawn"
        })
        print("✅ Usuario administrador creado en MongoDB Atlas")
    else:
        print("ℹ️ El usuario administrador ya existe.")

if __name__ == "__main__":
    create_initial_admin()