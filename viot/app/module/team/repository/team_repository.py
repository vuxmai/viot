from typing import NamedTuple
from uuid import UUID

from sqlalchemy import delete, exists, select

from app.database.repository import CrudRepository
from app.module.auth.model.permission import Permission
from app.module.auth.model.role import Role
from app.module.auth.model.role_permission import RolePermission
from app.module.auth.model.user_team_role import UserTeamRole

from ..model.team import Team


class TeamWithRoleAndPermissions(NamedTuple):
    team: Team
    role: str
    permissions: set[str]


class TeamRepository(CrudRepository[Team, UUID]):
    async def find_teams_with_role_by_user_id(
        self, user_id: UUID
    ) -> list[TeamWithRoleAndPermissions]:
        stmt = (
            select(Team, Role.name, Permission.scope)
            .join(UserTeamRole, UserTeamRole.team_id == Team.id)
            .join(Role, Role.id == UserTeamRole.role_id)
            .join(RolePermission, RolePermission.role_id == Role.id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(UserTeamRole.user_id == user_id)
        )

        result: dict[UUID, TeamWithRoleAndPermissions] = {}
        for team, role, permission in (await self.session.execute(stmt)).all():
            if team.id not in result:
                result[team.id] = TeamWithRoleAndPermissions(
                    team=team, role=role, permissions=set()
                )
            result[team.id].permissions.add(permission)

        return list(result.values())
        # return [
        #     TeamWithRoleAndPermission(team=team, role=role)
        #     for team, role in (await self.session.execute(stmt)).all()
        # ]

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
