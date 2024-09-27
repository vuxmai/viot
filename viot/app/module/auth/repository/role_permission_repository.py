from sqlalchemy import insert

from app.database.repository import CrudRepository
from app.module.auth.model.role_permission import RolePermission


class RolePermissionRepository(CrudRepository[RolePermission, tuple[int, int]]):
    async def bulk_save(self, role_permissions: list[dict[str, int]]) -> None:
        stmt = insert(RolePermission).values(role_permissions)
        await self.session.execute(stmt)
