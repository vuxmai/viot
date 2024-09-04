from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_AUTH_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    JWT_SECRET: str


@lru_cache
def get_auth_settings() -> AuthSettings:
    return AuthSettings()  # type: ignore


auth_settings: AuthSettings = get_auth_settings()
