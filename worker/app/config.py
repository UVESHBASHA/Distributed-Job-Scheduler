import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite://")
    WORKER_NAME: str = os.getenv("WORKER_NAME", "worker-1")
    HEARTBEAT_INTERVAL: int = 10
    POLL_INTERVAL: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
