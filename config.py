from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    MODE: Literal['TEST', "LOCAL", "DEV", "PROD"] = "LOCAL"
    NUM_WORKERS: int

    DB_PASSWORD: str
    DB_USER: str
    DB_DB: str
    DB_HOST: str
    DB_PORT: str

    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    LOGGER_STDOUT: bool
    LOGGER_SERIALIZE: bool
    LOG_ENQUEUE: bool
    LOG_ROTATION: bool
    ADD_VALIDATION_ERRORS_TO_RESPONSES: bool

    @property
    def db_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DB}"

    @property
    def db_url_sync(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DB}"

    class Config:
        env_file = BASE_DIR / ".env.sample"


settings = Settings()
