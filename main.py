from fastapi import FastAPI
from routes import user_routes
from routes import task_routes
from fastapi.middleware.cors import CORSMiddleware

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