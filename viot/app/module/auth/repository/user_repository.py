from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, exists, select, update

from app.database.repository import CrudRepository

from ..model.user import User


class UserRepository(CrudRepository[User, UUID]):
    async def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return (await self.session.execute(stmt)).scalar()

    async def find_id_by_email(self, email: str) -> UUID | None:
        stmt = select(User.id).where(User.email == email)
        return (await self.session.execute(stmt)).scalar()

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(exists().where(User.email == email))
        result = await self.session.execute(stmt)
        return result.scalar() or False

    async def update_password(self, user_id: UUID, hashed_password: bytes) -> None:
        stmt = update(User).where(User.id == user_id).values(password=hashed_password)
        await self.session.execute(stmt)

    async def update_email_verified_at(self, user_id: UUID, email_verified_at: datetime) -> None:
        stmt = update(User).where(User.id == user_id).values(email_verified_at=email_verified_at)
        await self.session.execute(stmt)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = delete(User).where(User.id == id)
        await self.session.execute(stmt)
