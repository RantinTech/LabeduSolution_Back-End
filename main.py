from fastapi import FastAPI
from routes import user_routes
from routes import task_routes
from routes import ai
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from services.task_ai_service import run_task_monitor

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
app.include_router(ai.router)

scheduler = BackgroundScheduler()
scheduler.add_job(run_task_monitor, "interval", minutes=30)
scheduler.start()