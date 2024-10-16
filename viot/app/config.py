from functools import lru_cache
from typing import Any, Literal

from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import __version__


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    PROJECT_NAME: str = "Viot"

    ENV: Literal["dev", "prod"] = "dev"
    WORKERS: int = 1
    DOMAIN: str
    API_DOMAIN: str
    UI_URL: str

    API_PORT: int = 8000
    API_PREFIX: str = ""
    API_INTERNAL_PREFIX: str = "/internal"

    ALLOW_CREDENTIALS: bool = True
    ALLOW_CORS_ORIGINS: list[AnyHttpUrl | str] = []
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_CORS_HEADERS: list[str] = ["*"]

    @computed_field  # type: ignore
    @property
    def API_SERVER_URL(self) -> str:
        if self.ENV == "dev":
            return f"http://{self.API_DOMAIN}"
        return f"https://{self.API_DOMAIN}"

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
def get_app_settings() -> AppSettings:
    return AppSettings()  # type: ignore


app_settings: AppSettings = get_app_settings()
