from fastapi import APIRouter
from services.email_alert_service import send_emails_for_overdue_tasks
from services.email_ml_service import run_task_monitor_ml

router = APIRouter(
    prefix="/send_email",
    tags=["email"]
    )

@router.get("/check-deadlines")
def run_auto():
    response = send_emails_for_overdue_tasks()
    return response

@router.get("/check-risk")
def run_ml_email():
    """Envia emails de tarefas futuras com risco de atraso"""
    result = run_task_monitor_ml()
    return result