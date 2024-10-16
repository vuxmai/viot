from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class EmqxSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_EMQX_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    API_URL: str
    API_KEY: str
    SECRET_KEY: str

    MQTT_WHITELIST_FILE_PATH: str = ""


@lru_cache
def get_emqx_settings() -> EmqxSettings:
    return EmqxSettings()  # type: ignore


emqx_settings: EmqxSettings = get_emqx_settings()
