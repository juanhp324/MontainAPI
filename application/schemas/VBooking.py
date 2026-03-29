from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type
from typing import Optional, List

class Sleeper_Persons(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Nombre completo de la persona que se hospedará",
        examples=["Juan Pérez"]
    )

class Booking_Create(BaseModel):
    date: date_type = Field(..., description="Fecha de la reserva en formato YYYY-MM-DD", examples=["2026-12-31"])
    type: str = Field(..., pattern="^(pass_day|sleep)$", description="Tipo de reserva: pasadía o alojamiento", examples=["sleep"])
    names_sleepers: List[Sleeper_Persons] = Field(..., min_length=1, description="Lista de personas incluidas en la reserva")
    include_food: bool = Field(False, description="Indica si se incluye el servicio de alimentación")
    comments: Optional[str] = Field(None, max_length=500, description="Observaciones adicionales para la reserva")

    @field_validator('date')
    @classmethod
    def date_must_be_future(cls, v):
        if v < date_type.today():
            raise ValueError('La fecha debe ser hoy o en el futuro')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-12-31",
                "type": "sleep",
                "names_sleepers": [{"name": "Juan Pérez"}],
                "include_food": True,
                "comments": "Requerimos habitación cerca de la piscina."
            }
        }