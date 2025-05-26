import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_SANDBOX_NUMBER: str
    TWILIO_TEMPLATE_SID: str
    CONTENT_VARIABLES: str

    @property
    def content_variables_dict(self) -> dict:
        return json.loads(self.CONTENT_VARIABLES)

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
