from functools import lru_cache

from httpx import BasicAuth
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmqxSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_EMQX_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    API_URL: str
    API_KEY: str
    SECRET_KEY: str

    MQTT_WHITELIST_FILE_PATH: str = ""

    @computed_field  # type: ignore
    @property
    def BASIC_AUTH(self) -> BasicAuth:
        return BasicAuth(username=self.API_KEY, password=self.SECRET_KEY)


@lru_cache
def get_emqx_settings() -> EmqxSettings:
    return EmqxSettings()  # type: ignore


emqx_settings: EmqxSettings = get_emqx_settings()
