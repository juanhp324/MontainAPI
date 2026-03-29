# MountainAPI - Sistema de Gestión de Reservas (Premium v2.1)

Este proyecto es una API de alto rendimiento construida con FastAPI y MongoDB para gestionar reservas de pasadía y alojamiento.

## 🚀 Características Avanzadas (v2.1)

- **Resiliencia (Circuit Breaker):** Implementación del patrón *Circuit Breaker* en todas las operaciones de base de datos para prevenir fallos en cascada y mejorar la disponibilidad.
- **Rate Limiting Global:** Límite estricto de **100 solicitudes por minuto por IP** para proteger contra abusos coordinados.
- **Seguridad Robusta:** Hashing de contraseñas con `bcrypt`, autenticación JWT con soporte para **Refresh Tokens** y control de acceso basado en roles (RBAC).
- **Testing Automatizado:** Suite completa de pruebas de integración con `pytest` y `mongomock` (no requiere base de datos real para ejecutarse).
- **Observabilidad:** Logging estructurado con identificadores de solicitud y manejo global de excepciones.
- **Documentación Premium:** OpenAPI/Swagger totalmente documentado con ejemplos, tipos y descripciones detalladas.

## 🛠 Instalación y Configuración

1. **Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Entorno (.env):**
   ```env
   MONGO_URI=mongodb://...
   SECRET_KEY=tu_llave_secreta
   ADMIN_EMAIL=admin@ejemplo.com
   ADMIN_PASSWORD=password_seguro
   ALLOWED_ORIGINS=http://localhost:3000
   ```

3. **Inicialización:**
   ```bash
   python init_db.py
   ```

4. **Ejecutar Pruebas:**
   ```bash
   pytest tests/
   ```

5. **Servidor:**
   ```bash
   python -m uvicorn application.main:app --reload
   ```

## 📄 Documentación Interactiva
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
