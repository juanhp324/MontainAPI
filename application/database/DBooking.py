from .connection import bookings_col
from bson import ObjectId
from application.core.resilience import db_circuit


@db_circuit
def save_reservation(new_reservation: dict):
    result = bookings_col.insert_one(new_reservation)
    new_reservation["id"] = str(result.inserted_id)
    # Eliminamos el _id nativo para evitar problemas de serialización en FastAPI
    if "_id" in new_reservation:
        del new_reservation["_id"]
    return new_reservation

@db_circuit
def get_all_reservations():
    reservations = list(bookings_col.find())
    for r in reservations:
        r["id"] = str(r["_id"]) 
        del r["_id"]
    return reservations

@db_circuit
def get_reservation_by_id(reservation_id: str):
    """Busca una reserva usando el ObjectId nativo de MongoDB."""
    try:
        res = bookings_col.find_one({"_id": ObjectId(reservation_id)})
        if res:
            res["id"] = str(res["_id"])
            del res["_id"]
        return res
    except Exception:
        return None

@db_circuit
def update_reservation_status(reservation_id: str, new_state: str):
    """Actualiza el estado de una reserva usando su ObjectId."""
    try:
        result = bookings_col.update_one(
            {"_id": ObjectId(reservation_id)}, 
            {"$set": {"state": new_state}}
        )
        if result.matched_count == 0:
            return None
        return get_reservation_by_id(reservation_id)
    except Exception:
        return None