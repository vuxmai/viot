from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_CELERY_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    REDIS_SERVER: str = "localhost"
    REDIS_PORT: int = 6379

    BROKER_REDIS_DATABASE: int
    BACKEND_REDIS_DATABASE: int

    BACKEND_REDIS_PREFIX: str = "viot:celery"
    BACKEND_REDIS_TIMEOUT: float = 5.0

    TASK_PACKAGES: list[str] = [
        "app.celery_worker.tasks",
    ]

    @computed_field  # type: ignore
    @property
    def BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.BROKER_REDIS_DATABASE}"

    @computed_field  # type: ignore
    @property
    def RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.BACKEND_REDIS_DATABASE}"


@lru_cache
def _get_settings() -> CelerySettings:
    return CelerySettings()  # type: ignore


celery_settings = _get_settings()
