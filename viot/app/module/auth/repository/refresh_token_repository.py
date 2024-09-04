from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update

from app.database.repository.crud import CrudRepository
from app.module.auth.model.refresh_token import RefreshToken


class RefreshTokenRepository(CrudRepository[RefreshToken, int]):
    async def find_by_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def find_latest_token_by_user_id(self, user_id: UUID) -> str | None:
        stmt = (
            select(RefreshToken.token)
            .where(RefreshToken.user_id == user_id)
            .order_by(RefreshToken.expires_at.desc())
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_token_expires_at(self, token: str, expires_at: datetime) -> None:
        stmt = update(RefreshToken).where(RefreshToken.token == token).values(expires_at=expires_at)
        await self.session.execute(stmt)

    async def update_all_tokens_expires_at(self, user_id: UUID, expires_at: datetime) -> None:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(expires_at=expires_at)
        )
        await self.session.execute(stmt)
