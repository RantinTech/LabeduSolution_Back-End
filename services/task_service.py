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

def update_task_service(task_id: int, updates: TaskUpdate):
    data_to_update = {}

    if updates.descricao is not None:
        data_to_update["Description"] = updates.descricao

    if updates.status is not None:
        data_to_update["Status"] = updates.status

    if updates.prazo is not None:
        data_to_update["Date_Deadline"] = updates.prazo.isoformat()

    if updates.responsavel is not None:
        data_to_update["Responsible"] = updates.responsavel

    # caso nada tenha sido enviado
    if not data_to_update:
        return {"message": "Nenhum campo enviado para atualização"}

    # executa a atualização
    response = (
        supabase.table("Task")
        .update(data_to_update)
        .eq("id", int(task_id))
        .execute()
    )

    return {
        "message": "Tarefa atualizada com sucesso",
        "updated_fields": data_to_update,
        "task": response.data
    }


def delete_task_service(task_id: int):

    # executa a atualização
    response = (
        supabase.table("Task")
        .delete()
        .eq("id", int(task_id))
        .execute()
    )

    return {
        "message": "Tarefa deletada com sucesso",
        "deleted_task": response.data
    }
