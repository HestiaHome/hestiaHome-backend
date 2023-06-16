import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str

    SECRET_KEY: str

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        env_file_encoding = 'utf-8'


settings = Settings()
