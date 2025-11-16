from fastapi import APIRouter, HTTPException
from models.user_login import UserLogin
from services.user_service import UserService
from models.user_response import LoginResponse

router = APIRouter(prefix="/login")

@router.post("", response_model=LoginResponse)
def login(data: UserLogin):
    user = UserService.login(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return user
