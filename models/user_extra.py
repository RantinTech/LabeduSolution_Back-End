from pydantic import BaseModel
from typing import Optional

class UserExtraData(BaseModel):
    id: str
    nome: str
    sobrenome: str
    cpf: str
    foto_perfil: Optional[str]
    data_cadastro: Optional[str]
    ultimo_acesso: Optional[str]
    is_admin: bool
