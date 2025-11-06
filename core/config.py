import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env se estiver rodando localmente

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
