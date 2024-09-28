from uuid import UUID

from sqlalchemy import select, text, update

from app.database.repository import AsyncSqlalchemyRepository

from ..model.user_team_role import UserTeamPermissionScopeView, UserTeamRole


class UserTeamRoleRepository(AsyncSqlalchemyRepository):
    async def is_user_has_permission_in_team(
        self, *, user_id: UUID, team_id: UUID, permission_scope: str
    ) -> bool:
        stmt = select(
            select(UserTeamPermissionScopeView)
            .where(
                text(
                    "user_id = :user_id "
                    "AND team_id = :team_id "
                    "AND permission_scope = :permission_scope"
                )
            )
            .exists()
        )
        result = await self.session.execute(
            stmt, {"user_id": user_id, "team_id": team_id, "permission_scope": permission_scope}
        )
        return bool(result.scalar())

    async def save(self, obj: UserTeamRole) -> UserTeamRole:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update_role_id(self, *, user_id: UUID, team_id: UUID, role_id: int) -> None:
        stmt = (
            update(UserTeamRole)
            .where(UserTeamRole.user_id == user_id, UserTeamRole.team_id == team_id)
            .values(role_id=role_id)
        )
        await self.session.execute(stmt)
