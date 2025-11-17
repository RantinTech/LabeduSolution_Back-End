from core.config import supabase
from models.task import Task
from schemas.task_schema import TaskCreate, TaskUpdate
import datetime

def list_task():
    response = supabase.table("Task").select("*").execute()
    return response.data

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