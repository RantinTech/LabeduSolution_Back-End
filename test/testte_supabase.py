from supabase import create_client, Client
import os
from dotenv import load_dotenv

# --- CARREGAR VARIÁVEIS DE AMBIENTE ---
load_dotenv()  # carrega o arquivo .env se existir

# --- CONFIGURAÇÕES DO SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # use a service key para inserir dados protegidos

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ As variáveis SUPABASE_URL e SUPABASE_SERVICE_KEY precisam estar configuradas.")

# --- CONEXÃO COM O SUPABASE ---
def conectar_supabase() -> Client:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Conectado ao Supabase com sucesso!")
    return supabase


# --- FUNÇÃO PARA INSERIR DADOS ---
def inserir_dado(supabase: Client):
    dados = {
        "Name": "Matheus Rantin",
        "Email": "matheus@example.com",
        "Password": "25",
        "Admin": True
    }

    try:
        resposta = supabase.table("User").insert(dados).execute()
        print("📤 Dado inserido com sucesso:", resposta.data)
    except Exception as e:
        print("❌ Erro ao inserir dado:", e)


# --- FUNÇÃO PARA LISTAR DADOS ---
def listar_dados(supabase: Client):
    try:
        resposta = supabase.table("User").select("*").execute()
        print("📥 Dados atuais na tabela:")
        for linha in resposta.data:
            print(linha)
    except Exception as e:
        print("❌ Erro ao listar dados:", e)


# --- EXECUÇÃO DO TESTE ---
if __name__ == "__main__":
    supabase = conectar_supabase()
    inserir_dado(supabase)
    listar_dados(supabase)
