from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from core.config import settings

security = HTTPBearer()


# ============================================================
# 🔐 Criar Token JWT
# ============================================================
def create_jwt_token(data: dict):
    """
    Gera um JWT com expiração configurada
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRES)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# ============================================================
# 🔐 Verificar Token
# ============================================================
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Valida o token enviado no header Authorization: Bearer
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload  # retorna sub, exp, etc.

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ============================================================
# 🔐 Obter usuário atual a partir do token
# ============================================================
def get_current_user(payload: dict = Depends(verify_token)):
    """
    Retorna o usuário autenticado (sub = ID do Supabase Auth)
    """
    if "sub" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload["sub"]
