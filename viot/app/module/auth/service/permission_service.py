from uuid import UUID

from injector import inject

from ..exception.permission_exception import ResourceAccessDeniedException
from ..repository.user_team_role_repository import UserTeamRoleRepository


class PermissionService:
    @inject
    def __init__(
        self,
        user_team_role_repository: UserTeamRoleRepository,
    ) -> None:
        self._user_team_role_repository = user_team_role_repository

    async def validate_user_access_team_resource(
        self, *, user_id: UUID, team_id: UUID, permission_scope: str
    ) -> None:
        if not await self._user_team_role_repository.is_user_has_permission_in_team(
            user_id=user_id, team_id=team_id, permission_scope=permission_scope
        ):
            raise ResourceAccessDeniedException
