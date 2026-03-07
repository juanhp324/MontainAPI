from .connection import bookings_col
from bson import ObjectId


def save_reservation(new_reservation: dict):
    result = bookings_col.insert_one(new_reservation)
    new_reservation["id"] = str(result.inserted_id)
    return new_reservation

def get_all_reservations():
    reservations = list(bookings_col.find())
    for r in reservations:
        r["id"] = str(r["_id"]) 
        del r["_id"]
    return reservations

def get_reservation_by_id(reservation_id: int):
    return bookings_col.find_one({"id": reservation_id})

def update_reservation_status(reservation_id: int, new_state: str):
    bookings_col.update_one(
        {"id": reservation_id}, 
        {"$set": {"state": new_state}}
    )
    return get_reservation_by_id(reservation_id)