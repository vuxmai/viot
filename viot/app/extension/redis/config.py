from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIOT_REDIS_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    SERVER: str = "localhost"
    PORT: int = 6379


@lru_cache
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


redis_settings = get_redis_settings()
