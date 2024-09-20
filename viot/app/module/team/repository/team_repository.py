from uuid import UUID

import msgspec
from sqlalchemy import delete, exists, select

from app.database.repository import CrudRepository
from app.module.auth.model.role import Role
from app.module.auth.model.user_team_role import UserTeamRole

from ..model.team import Team


class TeamWithRole(msgspec.Struct, frozen=True):
    team: Team
    role: str


class TeamRepository(CrudRepository[Team, UUID]):
    async def find_teams_with_role_by_user_id(self, user_id: UUID) -> list[TeamWithRole]:
        stmt = (
            select(Team, Role.name)
            .join(UserTeamRole, UserTeamRole.team_id == Team.id)
            .join(Role, Role.id == UserTeamRole.role_id)
            .where(UserTeamRole.user_id == user_id)
        )
        return [
            TeamWithRole(team=team, role=role)
            for team, role in (await self.session.execute(stmt)).all()
        ]

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(exists().where(Team.slug == slug))
        return bool((await self.session.execute(stmt)).scalar())

    async def exists_by_id(self, id: UUID) -> bool:
        stmt = select(exists().where(Team.id == id))
        return bool((await self.session.execute(stmt)).scalar())

    async def user_has_teams(self, user_id: UUID) -> bool:
        stmt = select(exists().where(UserTeamRole.user_id == user_id))
        return bool((await self.session.execute(stmt)).scalar())

    async def delete_by_id(self, id: UUID) -> None:
        await self.session.execute(delete(Team).where(Team.id == id))

    async def delete_all_by_user_id(self, user_id: UUID) -> None:
        stmt = (
            delete(Team)
            .where(Team.id == UserTeamRole.team_id)
            .where(UserTeamRole.user_id == user_id)
        )
        await self.session.execute(stmt)
