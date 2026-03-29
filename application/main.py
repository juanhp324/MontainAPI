import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from application.routes.RAuth import router as auth_router
from application.routes.RUser import router as user_router
from application.routes.RBooking import router as book_router
from fastapi.middleware.cors import CORSMiddleware
from application.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

load_dotenv()

# Configuración de Logging Estructurado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [RequestID: %(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger("MontainAPI")

app = FastAPI(
    title="MontainAPI - Premium Resort Management",
    description="""
    ## API de Gestión de Reservas Avanzada
    
    Esta API permite gestionar reservas de pasadía y alojamiento con:
    - **Seguridad:** Hashing bcrypt y RBAC (Roles).
    - **Resiliencia:** Patrón Circuit Breaker integrado.
    - **Escalabilidad:** Rate Limiting global y por endpoint.
    - **Documentación:** OpenAPI 3.0 compatible.
    """,
    version="2.1.0",
    contact={
        "name": "Juan HP - Senior Developer",
        "url": "https://github.com/juanhp324",
    },
    license_info={
        "name": "Propiedad de Montain Resort",
    }
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"ERROR CRÍTICO en {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Ocurrió un error interno en el servidor",
            "request_path": request.url.path
        },
    )

# Configuración de CORS restringida
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth_router) 
app.include_router(user_router)
app.include_router(book_router)

@app.get("/", tags=["General"])
def home():
    """Endpoint de salud del sistema."""
    return {"status": "online", "mensaje": "API Montain funcionando"}
