from application.database.DBooking import save_reservation ,update_reservation_status

PRICE_PASS_DAY = 500
PRICE_SLEEP_EXTRA = 1000
PRICE_FOOD_EXTRA = 350

def process_reservation(data):
    # Calculamos la cantidad automáticamente basándonos en la lista de nombres
    quantity = len(data.names_sleepers)

    total_cost = PRICE_PASS_DAY * quantity
    
    if data.type == "sleep":
        total_cost += (PRICE_SLEEP_EXTRA * quantity)
    
    if data.include_food:
        total_cost += (PRICE_FOOD_EXTRA * quantity)

    reserva_final = {
        "date": str(data.date),
        "type": data.type,
        "quantity": quantity,
        "names_sleepers": [p.name for p in data.names_sleepers],
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
