from sqlalchemy import select

from app.database.repository import CrudRepository
from app.module.auth.model.password_reset import PasswordReset


class PasswordResetRepository(CrudRepository[PasswordReset, str]):
    async def find_by_token(self, token: str) -> PasswordReset | None:
        stmt = select(PasswordReset).where(PasswordReset.token == token)
        return (await self.session.execute(stmt)).scalar_one_or_none()
