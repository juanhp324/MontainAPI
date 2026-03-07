from application.database.connection import users_col, bookings_col
import hashlib


def hash_password(password: str) -> str:
    """Hash simple con SHA-256. Suficiente para este proyecto."""
    return hashlib.sha256(password.encode()).hexdigest()


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
    admin_email = "juanhp324@gmail.com"
    admin_password = hash_password("juandenisse13")

    # Verificamos si ya existe para no duplicarlo
    existing = users_col.find_one({"email": admin_email})

    if not existing:
        users_col.insert_one({
            "email": admin_email,
            "password": admin_password,
            "nombre": "Administrador Respawn",
            "role": "admin"
        })
        print("✅ Usuario administrador creado en MongoDB Atlas")
    else:
        # Si existe pero tiene la contraseña en texto plano, la actualiza con hash
        if len(existing["password"]) != 64:  # SHA-256 = 64 caracteres hex
            users_col.update_one(
                {"email": admin_email},
                {"$set": {"password": admin_password, "role": "admin"}}
            )
            print("🔄 Contraseña del admin actualizada con hash seguro")
        else:
            print("ℹ️ El usuario administrador ya existe con contraseña segura.")


if __name__ == "__main__":
    create_indexes()
    create_initial_admin()