from uuid import UUID

from injector import inject
from sqlalchemy import select

from app.database.repository import CrudRepository
from app.extension.redis.client import RedisClient

from .constant import JWT_REFRESH_TOKEN_EXP, REDIS_REFRESH_TOKEN_PREFIX
from .model import PasswordReset


class PasswordResetRepository(CrudRepository[PasswordReset, str]):
    async def find_by_token(self, token: str) -> PasswordReset | None:
        stmt = select(PasswordReset).where(PasswordReset.token == token)
        return (await self.session.execute(stmt)).scalar_one_or_none()


class RefreshTokenRepository:
    @inject
    def __init__(self, redis_client: RedisClient) -> None:
        self._redis_client = redis_client

    async def save(self, *, user_id: UUID, token: str) -> None:
        key = f"{REDIS_REFRESH_TOKEN_PREFIX}:{user_id.hex}:{token}"
        await self._redis_client.setex(key, JWT_REFRESH_TOKEN_EXP, 0)

    async def delete(self, user_id: UUID, token: str) -> None:
        key = f"{REDIS_REFRESH_TOKEN_PREFIX}:{user_id.hex}:{token}"
        await self._redis_client.delete(key)

    async def exists(self, user_id: UUID, token: str) -> bool:
        key = f"{REDIS_REFRESH_TOKEN_PREFIX}:{user_id.hex}:{token}"
        return await self._redis_client.exists(key) == 1
