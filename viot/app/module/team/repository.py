from uuid import UUID

from sqlalchemy import exists, select

from app.database.repository import CrudRepository, PageableRepository

from .model import Team, UserTeam
from .projection import TeamWithRole


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


class UserTeamRepository(CrudRepository[UserTeam, tuple[UUID, UUID]]):
    async def find_role_name(self, user_id: UUID, team_id: UUID) -> str | None:
        stmt = select(UserTeam.role).where(UserTeam.user_id == user_id, UserTeam.team_id == team_id)
        return (await self.session.execute(stmt)).scalar()
