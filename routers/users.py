from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from core.config import settings
from services.user_service import supabase

router = APIRouter(prefix="/users")

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = supabase.table("User").select("*").eq("id", user_id).single().execute()

        return user.data

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/me")
def get_me(token: str):
    return get_current_user(token)
