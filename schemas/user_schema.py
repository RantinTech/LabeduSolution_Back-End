from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    cargo: Optional[str] = None
    foto: Optional[str] = None

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    foto: Optional[str] = None
    admin: Optional[bool] = None
