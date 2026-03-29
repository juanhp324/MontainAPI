from circuitbreaker import circuit
import logging

logger = logging.getLogger(__name__)

# Configuración del Circuit Breaker para la Base de Datos
# failure_threshold: número de fallos para abrir el circuito
# recovery_timeout: segundos para esperar antes de intentar cerrar el circuito (half-open)
db_circuit = circuit(failure_threshold=5, recovery_timeout=60)

def circuit_breaker_monitor(cb):
    """Callback para loguear cambios de estado del circuito."""
    logger.warning(f"Circuit Breaker {cb.name} cambió a estado: {cb.state}")

# Opcionalmente podemos registrar eventos si la librería lo permite de forma sencilla
# o simplemente envolver las llamadas.
