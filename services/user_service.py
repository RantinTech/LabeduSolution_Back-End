from supabase import create_client
from core.config import settings
from core.security import create_jwt_token
from datetime import datetime
from fastapi import HTTPException
from services.user_mapper import map_user_record
import uuid

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


class UserService:

    # ====================================================
    # REGISTER USER (AUTENTICAÇÃO + TABELA USER)
    # ====================================================
    @staticmethod
    def register(data):

        # 1. Criar usuário no Auth
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário no Auth")

        user_id = auth_response.user.id

        # 2. Criar registro na tabela User
        insert = supabase.table("User").insert({
            "id": user_id,
            "Name": data.nome,
            "Surname": data.sobrenome,
            "Cpf": data.cpf,
            "Photo_Profile": data.foto_perfil,
            "Date_Register": datetime.utcnow().isoformat(),
            "Date_Acess": None,
            "Admin": False
        }).execute()

        if not insert.data:
            raise HTTPException(status_code=400, detail="Erro ao salvar dados extras")

        # 3. Criar JWT
        token = create_jwt_token({"sub": user_id})

        # 4. Padronizar retorno
        mapped_user = map_user_record(insert.data[0])

        return {
            "token": token,
            "user": mapped_user
        }

    # ====================================================
    # LOGIN USER
    # ====================================================
    @staticmethod
    def login(email: str, password: str):

        # 1. Login AUTH
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not auth_response.user:
            return None

        user_id = auth_response.user.id

        # 2. Buscar dados adicionais
        row = supabase.table("User").select("*").eq("id", user_id).single().execute()

        if not row.data:
            raise HTTPException(status_code=404, detail="Usuário sem registros extras")

        # 3. Atualizar último acesso
        supabase.table("User").update({
            "Date_Acess": datetime.utcnow().isoformat()
        }).eq("id", user_id).execute()

        # 4. Criar token
        token = create_jwt_token({"sub": user_id})

        # 5. Retorno padronizado
        mapped_user = map_user_record(row.data)

        return {
            "token": token,
            "user": mapped_user
        }

    # ====================================================
    # LISTAR TODOS OS USERS (PARA ADMIN)
    # ====================================================
    @staticmethod
    def get_all_users():
        result = supabase.table("User").select("*").execute()

        if not result.data:
            return []

        users = []

        for u in result.data:
            users.append({
                "id": u.get("id"),
                "nome": u.get("Name"),
                "sobrenome": u.get("Surname"),
                "cpf": u.get("Cpf"),
                "email": u.get("Email") if "Email" in u else "",
                "foto": u.get("Photo_Profile"),
                "date_register": u.get("Date_Register"),
                "date_acess": u.get("Date_Acess"),
                "admin": u.get("Admin", False),
                "curso": "Não informado",
                "localidade": "Não informado",
                "formacoes": "",
                "avaliacao": 0,
                "tarefas": []
            })

        return users

    # ====================================================
    # CREATE USER (ADMIN)
    # ====================================================
    @staticmethod
    def create_user(data):

        new_id = str(uuid.uuid4())

        insert = supabase.table("User").insert({
            "id": new_id,
            "Name": data.nome,
            "Surname": data.sobrenome,
            "Cpf": data.cpf,
            "Photo_Profile": data.foto,
            "Date_Register": datetime.utcnow().isoformat(),
            "Date_Acess": None,
            "Admin": data.admin
        }).execute()

        if not insert.data:
            raise HTTPException(status_code=400, detail="Erro ao criar colaborador")

        return map_user_record(insert.data[0])

    # ====================================================
    # UPDATE USER
    # ====================================================
    @staticmethod
    def update_user(user_id: str, data):

        update_data = {
            "Name": data.nome,
            "Surname": data.sobrenome,
            "Cpf": data.cpf,
            "Photo_Profile": data.foto,
            "Admin": data.admin
        }

        result = supabase.table("User").update(update_data).eq("id", user_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return map_user_record(result.data[0])

    # ====================================================
    # DELETE USER
    # ====================================================
    @staticmethod
    def delete_user(user_id: str):

        result = supabase.table("User").delete().eq("id", user_id).execute()

        if result.data is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {"message": "Usuário removido com sucesso"}
