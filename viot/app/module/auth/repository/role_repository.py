from collections import defaultdict
from uuid import UUID

import msgspec
from sqlalchemy import delete, exists, func, select

from app.database.repository import CrudRepository

from ..model.permission import Permission
from ..model.role import Role
from ..model.role_permission import RolePermission


class RoleWithScopes(msgspec.Struct):
    role: Role
    scopes: set[str]


class RoleRepository(CrudRepository[Role, int]):
    async def is_role_name_exists_in_team(self, *, team_id: UUID, role_name: str) -> bool:
        stmt = select(exists().where(Role.name == role_name).where(Role.team_id == team_id))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def find_role_name_by_id(self, *, role_id: int) -> str | None:
        stmt = select(Role.name).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def find_all_by_team_id(self, *, team_id: UUID) -> list[RoleWithScopes]:
        stmt = (
            select(Role, Permission.scope)
            .join(RolePermission, RolePermission.role_id == Role.id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(Role.team_id == team_id)
        )
        results = (await self.session.execute(stmt)).fetchall()

        role_scopes_map: defaultdict[int, set[str]] = defaultdict(set)
        roles: dict[int, Role] = {}
        for row in results:
            role, scope = row.tuple()
            roles.setdefault(role.id, role)
            role_scopes_map[role.id].add(scope)

        return [
            RoleWithScopes(role=role, scopes=role_scopes_map[role.id]) for role in roles.values()
        ]

    async def find_role_id_by_role_name_and_team_id(
        self, *, team_id: UUID, role_name: str
    ) -> int | None:
        stmt = select(Role.id).where(Role.name == role_name).where(Role.team_id == team_id)
        return (await self.session.execute(stmt)).scalar()

    async def find_role_name_by_role_id_and_team_id(
        self, *, team_id: UUID, role_id: int
    ) -> str | None:
        stmt = select(Role.name).where(
            Role.id == role_id,
            Role.team_id == team_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def count_by_team_id(self, *, team_id: UUID) -> int:
        stmt = select(func.count()).where(Role.team_id == team_id)
        return (await self.session.execute(stmt)).scalar() or 0

    async def delete_by_id_and_team_id(self, *, role_id: int, team_id: UUID) -> None:
        stmt = delete(Role).where(Role.id == role_id).where(Role.team_id == team_id)
        await self.session.execute(stmt)
