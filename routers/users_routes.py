from fastapi import APIRouter, Depends, HTTPException
from services.user_service import UserService
from core.security import verify_token
from schemas.user_schema import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

# LISTAR TODOS OS COLABORADORES
@router.get("/")
def get_all_users(token: str = Depends(verify_token)):
    return UserService.get_all_users()

# CRIAR NOVO COLABORADOR
@router.post("/")
def create_user(data: UserCreate, token: str = Depends(verify_token)):
    return UserService.create_user(data)

# EDITAR COLABORADOR EXISTENTE
@router.put("/{user_id}")
def update_user(user_id: str, data: UserUpdate, token: str = Depends(verify_token)):
    return UserService.update_user(user_id, data)

# DELETAR COLABORADOR
@router.delete("/{user_id}")
def delete_user(user_id: str, token: str = Depends(verify_token)):
    return UserService.delete_user(user_id)
