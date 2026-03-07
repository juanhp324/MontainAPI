from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class Sleeper_Persons(BaseModel):
    name: str

class Booking_Create(BaseModel):
    date: date
    type: str = Field(..., pattern="^(pass_day|sleep)$")
    quantity: int
    names_sleepers: Optional[List[Sleeper_Persons]] = None 
    include_food: bool = False
    comments: Optional[str] = None