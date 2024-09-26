from uuid import UUID

import msgspec
from sqlalchemy import delete, exists, select

from app.database.repository import PageableRepository

from ..model.team import Team
from ..model.user_team import UserTeam


class TeamWithRole(msgspec.Struct, frozen=True):
    team: Team
    role: str


class TeamRepository(PageableRepository[Team, UUID]):
    async def find_teams_with_role_by_user_id(self, user_id: UUID) -> list[TeamWithRole]:
        stmt = select(Team, UserTeam.role).join(UserTeam).where(UserTeam.user_id == user_id)
        return [
            TeamWithRole(team=team, role=role)
            for team, role in (await self.session.execute(stmt)).all()
        ]

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(exists().where(Team.slug == slug))
        return bool((await self.session.execute(stmt)).scalar())

    async def user_has_teams(self, user_id: UUID) -> bool:
        stmt = select(exists().where(UserTeam.user_id == user_id))
        return bool((await self.session.execute(stmt)).scalar())

    async def delete_by_id(self, id: UUID) -> None:
        await self.session.execute(delete(Team).where(Team.id == id))
