from pydantic import BaseModel
from typing import Optional
from datetime import date
#Validação dos dados recebidos do front

class TaskCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = ""
    status: Optional[str] = "Pendente"
    responsible_id: Optional[str]
    data_prazo: Optional[date]

class TaskUpdate(BaseModel):
    descricao: Optional[str] = None
    status: str = None
    prazo: Optional[date] = None
    responsavel: Optional[str] = None