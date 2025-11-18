from core.config import supabase
from models.task import Task
from schemas.task_schema import TaskCreate, TaskUpdate
import datetime

def list_task():
    task_res = supabase.table("Task").select("*").execute()
    tasks = task_res.data
    full_task = []

    for task in tasks:
        responsible_id = task.get("Responsible")
        
        user_res = supabase.table("User").select("*").eq("id", responsible_id).single().execute()
        user_data = user_res.data if user_res.data else None

        full_task.append({
            **task,
            "Colaborador": user_data
        })
    return full_task

def create_task(task: TaskCreate):
    response = supabase.table("Task").insert({
        "Date_Create": datetime.date.today().isoformat(),
        "Manager": "Juliano",
        "Title": task.titulo,
        "Description": task.descricao,
        "Status": task.status,
        "Date_Deadline": task.data_prazo.isoformat(),
        "Responsible": task.responsible_id
    }).execute()
    return response.data

def update_task_status(task_id: int, status: str):
    response = supabase.table("Task").update({"Status": status}).eq("id", int(task_id)).execute()
    return response.data