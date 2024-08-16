from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_EMAIL_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_USER: str
    SMTP_PASSWORD: str


@lru_cache
def _get_settings() -> EmailSettings:
    return EmailSettings()  # type: ignore


email_settings = _get_settings()
