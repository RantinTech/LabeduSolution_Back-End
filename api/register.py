from fastapi import FastAPI, Request
from models.user_model import UserRegister
from services.user_service import register_user

app = FastAPI()

@app.post("/api/register")
async def register(data: UserRegister):
    result = register_user(data.name, data.email, data.password)
    return result
