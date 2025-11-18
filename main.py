from fastapi import FastAPI
from routes import user_routes
from routes import task_routes
from routes import alert_email
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from services.email_ml_service import run_task_monitor_ml
from services.email_alert_service import send_emails_for_overdue_tasks

app = FastAPI(
    title="Task Manager API",
    description="API de gestão de tarefas usando Fast + Supabase",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers = ["*"]
)

app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(alert_email.router)

scheduler = BackgroundScheduler()

# Envia emails de tarefas atrasadas a cada 30 min
scheduler.add_job(send_emails_for_overdue_tasks, "interval", minutes=30)

# Envia emails de tarefas futuras com risco de atraso (ML) a cada 30 min
scheduler.add_job(run_task_monitor_ml, "interval", minutes=30)

scheduler.start()