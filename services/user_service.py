from core.config import supabase
from schemas.user_schema import UserLogin, UserCreate, UserUpdate
from postgrest.exceptions import APIError
from typing import Optional


def create_user(user: UserCreate):
    auth_res = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password
    })

    if not auth_res.user:
        raise Exception("Erro ao criar usuário no Supabase Auth")

    user_id = auth_res.user.id
    try:
        supabase.table("User").insert({
            "id": user_id,
            "Name": user.name,
            "Email": user.email
        }).execute()
    except APIError as e:
        # rollback: remove user do auth se falhar
        supabase.auth.admin.delete_user(user_id)
        raise Exception(f"Erro ao inserir dados extras: {e}")

    return {
        "id": user_id,
        "email": user.email,
        "name": user.name
    }


def login_user(user: UserLogin):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        user_id = res.user.id

        user_data = supabase.table("User").select("*").eq("id", user_id).single().execute()

        if not user_data.data:
            return None

        is_admin = user_data.data.get("Admin")

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user_id": res.user.id,
            "email": res.user.email,
            "is_admin": is_admin

        }

    except Exception:
        return None

def list_user():
    response = supabase.table("User").select("*").execute()
    return response.data

def update_user(user_id: str, updates: UserUpdate):
    data_to_update = {}

    if updates.nome is not None:
        data_to_update["Name"] = updates.nome

    if updates.sobrenome is not None:
        data_to_update["Surname"] = updates.sobrenome

    if updates.nome is not None:
        data_to_update["Email"] = updates.nome

    if updates.nome is not None:
        data_to_update["Admin"] = updates.nome

    if updates.nome is not None:
        data_to_update["Name"] = updates.nome
