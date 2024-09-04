from uuid import UUID

from sqlalchemy import select

from app.database.repository import CrudRepository

from ..model.user_team import UserTeam


class UserTeamRepository(CrudRepository[UserTeam, tuple[UUID, UUID]]):
    async def find_role_name(self, user_id: UUID, team_id: UUID) -> str | None:
        stmt = select(UserTeam.role).where(UserTeam.user_id == user_id, UserTeam.team_id == team_id)
        return (await self.session.execute(stmt)).scalar()
