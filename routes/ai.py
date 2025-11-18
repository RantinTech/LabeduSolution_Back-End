from fastapi import APIRouter
from services.task_ai_service import run_task_monitor

router = APIRouter(prefix="/ai", tags=["IA"])

@router.get("/run")
def run_ai():
    result = run_task_monitor()
    return result
