from pydantic import BaseModel, EmailStr

class UserAuthData(BaseModel):
    id: str
    email: EmailStr
