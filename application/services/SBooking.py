from application.database.DBooking import save_reservation ,update_reservation_status

PRICE_PASS_DAY = 500
PRICE_SLEEP_EXTRA = 1000
PRICE_FOOD_EXTRA = 350

def process_reservation(data):
    if data.type == "sleep" and (not data.names_sleepers or len(data.names_sleepers) == 0):
        return {"error": "Para reservar alojamiento debes proporcionar los nombres de las personas."}

    total_cost = PRICE_PASS_DAY * data.quantity
    
    if data.type == "sleep":
        total_cost += (PRICE_SLEEP_EXTRA * data.quantity)
    
    if data.include_food:
        total_cost += (PRICE_FOOD_EXTRA * data.quantity)

    reserva_final = {
        "date": str(data.date),
        "type": data.type,
        "quantity": data.quantity,
        "names_sleepers": [p.name for p in data.names_sleepers] if data.names_sleepers else [],
        "include_food": data.include_food,
        "total_to_pay": total_cost,
        "state": "pending"
    }
    
    return save_reservation(reserva_final)

def change_status(reservation_id: int, new_state: str):

    valid_states = ["confirmed", "canceled", "completed"]
    if new_state not in valid_states:
        return {"error": "Estado no válido"}
    
    result = update_reservation_status(reservation_id, new_state)
    if not result:
        return {"error": "Reserva no encontrada"}
    
    return result
