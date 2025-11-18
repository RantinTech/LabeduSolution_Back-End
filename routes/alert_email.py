from fastapi import APIRouter
from services.email_service import run_task_monitor_ml

router = APIRouter(
    prefix="/send_email",
    tags=["email"]
    )

@router.get("/check-deadlines")
def run_auto():
    response = run_task_monitor_ml()
    return {"status": "executado", "result": response}