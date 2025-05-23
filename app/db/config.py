from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "password"
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "postgresql://user:password@db:5432/luestilo"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    class Config:
        env_file = ".env"

settings = Settings()
