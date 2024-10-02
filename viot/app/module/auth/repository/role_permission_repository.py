from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.database.repository import CrudRepository
from app.module.auth.model.role_permission import RolePermission


class RolePermissionRepository(CrudRepository[RolePermission, tuple[int, int]]):
    async def bulk_save(self, role_permissions: list[dict[str, int]]) -> None:
        stmt = insert(RolePermission).values(role_permissions)
        await self.session.execute(stmt)

    async def bulk_save_on_conflict_do_nothing(
        self, role_permissions: list[dict[str, int]]
    ) -> None:
        stmt = (
            pg_insert(RolePermission)
            .values(role_permissions)
            .on_conflict_do_nothing(index_elements=["role_id", "permission_id"])
        )
        await self.session.execute(stmt)
