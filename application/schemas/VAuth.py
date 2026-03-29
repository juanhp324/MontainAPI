from pydantic import BaseModel, EmailStr, Field

class Login_Schema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="La contraseña debe tener al menos 8 caracteres")