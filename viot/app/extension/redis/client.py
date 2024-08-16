import logging
import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from .config import redis_settings

logger = logging.getLogger(__name__)


class RedisClient(Redis):  # type: ignore
    def __init__(self) -> None:
        super().__init__(
            host=redis_settings.SERVER,
            port=redis_settings.PORT,
            socket_timeout=5,
            decode_responses=True,
        )

    async def open(self) -> None:
        try:
            await self.ping()
        except TimeoutError:
            logger.error("Redis connection timeout")
            sys.exit(1)
        except AuthenticationError:
            logger.error("Redis authentication error")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            sys.exit(1)
        logger.info("Connected to Redis")


# For easier testing
def get_redis_client() -> RedisClient:
    return RedisClient()
