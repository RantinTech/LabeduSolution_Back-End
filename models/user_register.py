from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    nome: str
    sobrenome: str
    cpf: str
    foto_perfil: Optional[str] = None
