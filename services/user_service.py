# services/user_service.py
from core.database import supabase

def register_user(name: str, email: str, password: str):
    return supabase.auth.sign_up({
        "email": email,
        "password": password,
        "data": {"name": name}
    })
