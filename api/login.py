from fastapi import FastAPI
from models.user_model import UserLogin
from services.user_service import login_user

app = FastAPI()

@app.post("/api/login")
async def login(data: UserLogin):
    result = login_user(data.email, data.password)
    return result
