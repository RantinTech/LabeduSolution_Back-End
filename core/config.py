from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET: str = "supersecret123"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES: int = 60 * 24  # 24 horas

    class Config:
        env_file = ".env"

settings = Settings()
