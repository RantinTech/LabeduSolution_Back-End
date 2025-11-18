from core.config import supabase
from schemas.user_schema import UserLogin, UserCreate, UserUpdate
from postgrest.exceptions import APIError
from typing import Optional
from datetime import date


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
            "Email": user.email,
            "Surname": user.surname,
            "Locality": user.locality,
            "Course": user.course,
            "Cpf": user.cpf,
            "Password": user.password,
            "Date_Register": date.today().isoformat(),
            "Admin": user.admin,
            "Assessment": float(5.0)
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
        name_user = user_data.data.get("Name")
        photo_user = user_data.data.get("Photo_Profile")

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user_id": res.user.id,
            "name_user": name_user,
            "photo_user": photo_user,
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
            "id": u.get("id"),
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


def update_user_service(user_id: str, updates: UserUpdate):
    data_to_update = {}

    if updates.nome not in (None, ""):
        data_to_update["Name"] = updates.nome

    if updates.sobrenome not in (None, ""):
        data_to_update["Surname"] = updates.sobrenome

    if updates.email not in (None, ""):
        data_to_update["Email"] = updates.email

    if updates.admin is not None:
        data_to_update["Admin"] = updates.admin

    if updates.foto not in (None, ""):
        data_to_update["Photo_Profile"] = updates.foto

    # caso nenhum campo tenha sido enviado
    if not data_to_update:
        return {"message": "Nenhum dado enviado para atualização"}
    
    try:
        # atualiza na tabela "User"
        supabase.table("User").update(data_to_update).eq("id", user_id).execute()

        # se o email foi alterado, atualiza também no Auth
        if updates.email not in (None, ""):
            supabase.auth.admin.update_user_by_id(user_id, {
                "email": updates.email
            })

        return {
            "message": "Usuário atualizado com sucesso",
            "updated_fields": data_to_update
        }
    
    except APIError as e:
        raise Exception(f"Erro ao atualizar usuário: {str(e)}")
