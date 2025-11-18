import os
from datetime import datetime, timezone
from supabase import create_client, Client
import smtplib
from email.mime.text import MIMEText

# --- Configurações ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# EMAIL SMTP
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_alert_email(to_email: str, task_name: str, status: str):
    """Envia e-mail ao responsável pela tarefa"""

    msg = MIMEText(f"""
Olá!

A tarefa **{task_name}** está com status: **{status}**.

Por favor, revise e atualize no sistema.

Atenciosamente,  
IA do Sistema de Tarefas
""")

    msg["Subject"] = f"[ALERTA] Situação da tarefa: {task_name}"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print(f"E-mail enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def parse_deadline(date_str: str):
    """Converte deadline vindo do Supabase para datetime seguro"""
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        return None


def analyze_task(task: dict):
    """Analisa risco, atraso e status"""

    # Campos obrigatórios
    if "Date_Deadline" not in task or task["Date_Deadline"] is None:
        return task["Status"]

    deadline = parse_deadline(task["Date_Deadline"])
    if deadline is None:
        return task["Status"]

    now = datetime.now(timezone.utc)
    status = task["Status"]
    

    # Regra: atraso
    if now > deadline and status != "Atrasada":
        return "Atrasada"

    return status


def run_task_monitor():
    """IA principal — monitora tarefas"""

    print("🔍 IA monitorando tarefas...")

    response = supabase.table("Task").select("*").execute()
    tasks = response.data

    if not tasks:
        return {"message": "Nenhuma tarefa encontrada"}

    for task in tasks:
        new_status = analyze_task(task)

        if new_status != task["Status"]:

            # atualiza no banco
            supabase.table("Task").update({
                "Status": new_status
            }).eq("id", task["id"]).execute()

            # envia email, se houver email do responsável
            if "Email" in task and task["Email"]:
                send_alert_email(
                    to_email=task["Email"],
                    task_name=task.get("Name", "Tarefa sem nome"),
                    status=new_status
                )

            print(f"Tarefa {task['id']} atualizada para {new_status}")

    return {"message": "Monitoramento concluído", "data prazo": task["Date_Deadline"]}
