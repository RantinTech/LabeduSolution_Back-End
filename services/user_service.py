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
    # Buscar todos os usuários
    users_res = supabase.table("User").select("*").execute()
    users = users_res.data

    formatted_users = []

    for u in users:
        user_id = u.get("id")

        # Buscar tarefas do usuário
        tasks_res = supabase.table("Task").select("*").eq("Responsible", user_id).execute()
        tasks = tasks_res.data if tasks_res.data else []

        # Formatar tarefas
        formatted_tasks = [
            {
                "titulo": t.get("Title"),
                "prazo": t.get("Date_Deadline"),
                "status": t.get("Status"),
            }
            for t in tasks
        ]

        # Montar objeto final no formato solicitado
        formatted_users.append({
            "nome": u.get("Name"),
            "curso": u.get("Course"),
            "localidade": u.get("Locality"),
            "cpf": u.get("Cpf"),
            "email": u.get("Email"),
            "foto": u.get("Photo_Profile"),
            "avaliacao": u.get("Assessment", 0),
            "tarefas": formatted_tasks
        })

    return formatted_users


def update_user(user_id: str, updates: UserUpdate):
    data_to_update = {}

    if updates.nome is not None:
        data_to_update["Name"] = updates.nome

    if updates.sobrenome is not None:
        data_to_update["Surname"] = updates.sobrenome

    if updates.email is not None:
        data_to_update["Email"] = updates.nome

    if updates.admin is not None:
        data_to_update["Admin"] = updates.nome

    if updates.foto is not None:
        data_to_update["Photo_Profile"] = updates.nome

    if not data_to_update:
        return {"message": "Nenhum dado enviado para atualização"}
    
    try:
        supabase.table("User").update(data_to_update).eq("id", user_id).execute()

        if updates.email is not None:
            supabase.auth.admin.update_user_by_id(user_id, {
                "email":updates.email
            })

        return {
            "message": "Usuário atualizado com sucesso",
            "updated_fields": data_to_update
        }
    
    except APIError as e:
        raise Exception(f"Erro ao atualizar usuário: {e}")