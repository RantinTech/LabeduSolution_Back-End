from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserLogin, UserCreate
from services.user_service import create_user, login_user, list_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def register_user(user: UserCreate):
    result = create_user(user)
    return {"user": result}


@router.post("/login")
def login(user: UserLogin):
    result = login_user(user)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return result

@router.get("/list_users")
def users():
    return {"users": list_user()}