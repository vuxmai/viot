from functools import lru_cache

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ).unicode_string()


@lru_cache
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()  # type: ignore


db_settings: DatabaseSettings = get_db_settings()
