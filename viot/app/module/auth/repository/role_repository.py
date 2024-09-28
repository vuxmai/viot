from uuid import UUID

from sqlalchemy import exists, select

from app.database.repository import CrudRepository
from app.module.auth.model.role import Role


class RoleRepository(CrudRepository[Role, int]):
    async def is_role_name_exists_in_team(self, *, team_id: UUID, role_name: str) -> bool:
        stmt = select(exists().where(Role.name == role_name).where(Role.team_id == team_id))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

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
