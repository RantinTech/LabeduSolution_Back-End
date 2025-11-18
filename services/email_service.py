import os
from datetime import datetime, timezone
import pandas as pd
from supabase import create_client, Client
import smtplib
from email.mime.text import MIMEText
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- Configurações Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Configuração de Email ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


# --- Função para enviar email ---
def send_alert_email(to_email: str, task_name: str, deadline: str, probability: float):
    msg = MIMEText(f"""
Olá! 👋

A tarefa **{task_name}** está em risco de atraso:

📅 Prazo final: {deadline}
⚠️ Probabilidade de atraso: {probability*100:.1f}%

Por favor, revise e atualize o status no sistema.

Atenciosamente,  
Sistema de Monitoramento de Tarefas
""")

    msg["Subject"] = f"[ALERTA] Tarefa em risco: {task_name}"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print(f"Email enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


# --- Helper para converter datas ---
def parse_date(date_str: str):
    try:
        return pd.to_datetime(date_str.replace("Z", "+00:00"))
    except:
        return None


# --- Treina o modelo de ML ---
def train_model():
    """Treina modelo simples para prever risco de atraso"""
    response = supabase.table("Task").select("*").execute()
    tasks = response.data
    if not tasks:
        return None, None

    df = pd.DataFrame(tasks)

    # Criar target: 1 se já passou do prazo, 0 caso contrário
    df['Date_Deadline'] = pd.to_datetime(df['Date_Deadline'])
    df['Date_Create'] = pd.to_datetime(df['Date_Create'])
    now = pd.Timestamp.utcnow()

    df['target'] = (now > df['Date_Deadline']).astype(int)

    # Features simples: dias para o prazo, tempo desde criação
    df['days_to_deadline'] = (df['Date_Deadline'] - df['Date_Create']).dt.days
    df['days_since_create'] = (now - df['Date_Create']).dt.days

    X = df[['days_to_deadline', 'days_since_create']]
    y = df['target']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_scaled, y)

    return model, scaler


# --- Função principal de monitoramento ---
def run_task_monitor_ml():
    print("🔍 IA monitorando tarefas com ML...")

    model, scaler = train_model()
    if model is None:
        return {"message": "Nenhuma tarefa encontrada"}

    response = supabase.table("Task").select("*").execute()
    tasks = response.data
    now = pd.Timestamp.utcnow()

    for task in tasks:
        if not task.get("Date_Deadline") or not task.get("Email"):
            continue

        date_created = parse_date(task.get("Date_Create"))
        deadline = parse_date(task.get("Date_Deadline"))
        if not date_created or not deadline:
            continue

        days_to_deadline = (deadline - date_created).days
        days_since_create = (now - date_created).days
        X_pred = scaler.transform([[days_to_deadline, days_since_create]])

        prob = model.predict_proba(X_pred)[0][1]  # probabilidade de atraso

        # Envia email se probabilidade > 50%
        if prob > 0.5:
            send_alert_email(
                to_email=task["Email"],
                task_name=task.get("Title", "Tarefa sem nome"),
                deadline=task["Date_Deadline"],
                probability=prob
            )

    return {"message": "Monitoramento ML concluído"}
