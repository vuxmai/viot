from collections.abc import Sequence

from sqlalchemy import select

from app.database.repository import AsyncSqlalchemyRepository

from ..model.permission import Permission


class PermissionRepository(AsyncSqlalchemyRepository):
    async def find_permissions_by_scopes(self, scopes: set[str]) -> Sequence[Permission]:
        query = select(Permission).where(Permission.scope.in_(scopes))
        return (await self.session.execute(query)).scalars().all()

    async def find_all(self) -> Sequence[Permission]:
        query = select(Permission)
        return (await self.session.execute(query)).scalars().all()
