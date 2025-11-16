from pydantic import BaseModel
from typing import Optional

class UserExtraData(BaseModel):
    id: str
    name: str
    surname: str
    cpf: str
    photo_profile: Optional[str]
    date_register: Optional[str]
    date_acess: Optional[str]
    admin: bool

class LoginResponse(BaseModel):
    token: str
    user: UserExtraData
