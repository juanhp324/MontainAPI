
from pydantic import BaseModel, EmailStr

class Login_Schema(BaseModel):
    email: EmailStr
    password: str