from fastapi import APIRouter, HTTPException, Depends
from application.schemas.VBooking import Booking_Create
from application.services.SBooking import process_reservation
from application.core.security import get_current_user
from application.services.SBooking import change_status
from application.database.DBooking import get_all_reservations


router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/create")
def create_reservation(payload: Booking_Create):
    result = process_reservation(payload)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {
        "message": "Reserva procesada exitosamente",
        "detail": result
    }

@router.patch("/admin/manage/{reservation_id}")
def manage_reservation(reservation_id: int, new_state: str, admin: dict = Depends(get_current_user)):
    result = change_status(reservation_id, new_state)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return {
        "message": f"Reserva {reservation_id} actualizada a {new_state}",
        "detail": result
    }

@router.get("/admin/manage/all")
def list_all(admin: dict = Depends(get_current_user)):
    return get_all_reservations()