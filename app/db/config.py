from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "password"
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "postgresql://user:password@db:5432/luestilo"

    class Config:
        env_file = ".env"

settings = Settings()
