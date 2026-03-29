from slowapi import Limiter
from slowapi.util import get_remote_address

# Configuración global a 100 solicitudes por minuto por IP
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
