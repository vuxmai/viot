from functools import lru_cache
from typing import Any, Literal

from pydantic import AnyHttpUrl, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    PROJECT_NAME: str = "Viot"

    ENV: Literal["dev", "prod"] = "dev"
    WORKERS: int = 1
    DOMAIN: str = "localhost"
    UI_URL: str = "http://localhost:5173"

    API_PORT: int = 8000
    API_PREFIX: str = ""

    ALLOW_CREDENTIALS: bool = True
    ALLOW_CORS_ORIGINS: list[AnyHttpUrl | str] = [
        "http://localhost:5173",
    ]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_CORS_HEADERS: list[str] = ["*"]

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_REFRESH_TOKEN_SAMESITE: Literal["Strict", "Lax", "None"] = "Lax"
    JWT_REFRESH_TOKEN_SECURE: bool = True

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

    @computed_field  # type: ignore
    @property
    def FASTAPI_CONFIG(self) -> dict[str, Any]:
        return {
            "title": self.PROJECT_NAME,
            "description": self.PROJECT_NAME + " API documentation",
            "version": __version__,
            "redoc_url": None,
            "docs_url": "/docs",
            "openapi_url": "/docs/openapi.json",
        }


@lru_cache
def _get_settings() -> Settings:
    return Settings()  # type: ignore


settings: Settings = _get_settings()
