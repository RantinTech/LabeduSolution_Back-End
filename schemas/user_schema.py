from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    surname: Optional[str] = None
    photo_profile: Optional[str] = None
    password: str
    date_register: Optional[date] = None
    admin: Optional[bool] = False
    cpf: Optional[str] = None
    locality: Optional[str] = None
    course: Optional[str] = None
    avaliacao: Optional[float] = None


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
