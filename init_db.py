import os
import bcrypt
from dotenv import load_dotenv
from application.database.connection import users_col, bookings_col

load_dotenv()

def hash_password(password: str) -> str:
    """Hash seguro con bcrypt."""
    # Retornamos como string para guardar en MongoDB
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')


def create_indexes():
    """Crea índices en las colecciones para mejorar el rendimiento."""
    # Índice único en email → evita usuarios duplicados
    users_col.create_index("email", unique=True)
    print("✅ Índice único creado en users.email")

    # Índice en bookings por estado → acelera filtros de admin
    bookings_col.create_index("state")
    print("✅ Índice creado en bookings.state")

    # Índice en bookings por fecha → acelera búsquedas por día
    bookings_col.create_index("date")
    print("✅ Índice creado en bookings.date")


def create_initial_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password_raw = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password_raw:
        print("❌ Error: ADMIN_EMAIL o ADMIN_PASSWORD no definidos en .env")
        return

    admin_password = hash_password(admin_password_raw)

    # Verificamos si ya existe para no duplicarlo
    existing = users_col.find_one({"email": admin_email})

    if not existing:
        users_col.insert_one({
            "email": admin_email,
            "password": admin_password,
            "nombre": "Administrador Respawn",
            "role": "admin"
        })
        print(f"✅ Usuario administrador {admin_email} creado en MongoDB")
    else:
        # Si existe, actualizamos su contraseña al nuevo formato bcrypt y aseguramos el rol admin
        users_col.update_one(
            {"email": admin_email},
            {"$set": {"password": admin_password, "role": "admin"}}
        )
        print(f"🔄 Credenciales y rol de admin {admin_email} actualizados con bcrypt")


if __name__ == "__main__":
    create_indexes()
    create_initial_admin()