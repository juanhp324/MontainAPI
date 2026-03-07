from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class Sleeper_Persons(BaseModel):
    name: str

class Booking_Create(BaseModel):
    date: date
    type: str = Field(..., pattern="^(pass_day|sleep)$")
    names_sleepers: List[Sleeper_Persons] = Field(..., min_length=1)
    include_food: bool = False
    comments: Optional[str] = None