import os
from datetime import datetime
import pandas as pd
from supabase import create_client, Client
import smtplib
from email.mime.text import MIMEText

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_alert_email(to_email: str, task_name: str, deadline: str):
    """Envia email apenas para tarefas atrasadas"""
    msg = MIMEText(f"""
Olá! 👋

A tarefa **{task_name}** já está atrasada!

📅 Prazo final: {deadline}

Por favor, revise e atualize o status no sistema.

Atenciosamente,  
Sistema de Monitoramento de Tarefas
""")

    msg["Subject"] = f"[ALERTA] Tarefa atrasada: {task_name}"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print(f"Email enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


def send_emails_for_overdue_tasks():
    """Verifica tarefas atrasadas e envia email"""
    response = supabase.table("Task").select("*").execute()
    tasks = response.data
    now = pd.Timestamp.utcnow()

    for task in tasks:
        if not task.get("Date_Deadline") or not task.get("Email"):
            continue

        deadline = pd.to_datetime(task["Date_Deadline"], utc=True)
        if deadline < now:
            send_alert_email(
                to_email=task["Email"],
                task_name=task.get("Title", "Tarefa sem nome"),
                deadline=task["Date_Deadline"]
            )

    return {"message": "Emails enviados para tarefas atrasadas"}
