from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    cargo: Optional[str] = None
    photo_profile: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    foto: Optional[str] = None
    admin: Optional[bool] = None
