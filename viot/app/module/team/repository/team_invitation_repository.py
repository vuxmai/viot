from uuid import UUID

from sqlalchemy import delete, select

from app.database.repository import PageableRepository

from ..model.team_invitation import TeamInvitation


class TeamInvitationRepository(PageableRepository[TeamInvitation, UUID]):
    async def find_by_token(self, token: str) -> TeamInvitation | None:
        stmt = select(TeamInvitation).where(TeamInvitation.token == token)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def delete_by_token(self, token: str) -> None:
        stmt = delete(TeamInvitation).where(TeamInvitation.token == token)
        await self.session.execute(stmt)

    async def delete_by_id(self, id: UUID) -> None:
        stmt = delete(TeamInvitation).where(TeamInvitation.id == id)
        await self.session.execute(stmt)
