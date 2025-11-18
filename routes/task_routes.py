from fastapi import APIRouter
from schemas.task_schema import TaskCreate, TaskUpdate
from services.task_service import create_task, list_task, update_task_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/")
def get_tasks():
    return {"tasks": list_task()}

@router.post("/")
def add_task(task: TaskCreate):
    return {"task": create_task(task)}

@router.put("/{task_id}")
def update_task(task_id: int,task: TaskUpdate):
    return {"task": update_task_service(task_id, task)}