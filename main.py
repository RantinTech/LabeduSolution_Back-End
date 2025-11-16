from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.register import router as register_router
from routers.login import router as login_router
from routers.users_routes import router as users_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # front
    allow_credentials=True,
    allow_methods=["*"],   # <--- IMPORTANTE: Permite OPTIONS
    allow_headers=["*"],   # <--- IMPORTANTE
)

app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API running"}
