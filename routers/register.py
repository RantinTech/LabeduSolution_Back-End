from fastapi import APIRouter
from models.user_register import UserRegister
from services.user_service import UserService
from models.user_response import LoginResponse

router = APIRouter(prefix="/register")

@router.post("", response_model=LoginResponse)
def register_user(data: UserRegister):
    return UserService.register(data)
