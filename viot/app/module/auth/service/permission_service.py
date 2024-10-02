from uuid import UUID

from injector import inject

from ..dto.permission_dto import PermissionDto
from ..exception.permission_exception import ResourceAccessDeniedException
from ..repository.permission_repository import PermissionRepository
from ..repository.user_team_role_repository import UserTeamRoleRepository


class PermissionService:
    @inject
    def __init__(
        self,
        permission_repository: PermissionRepository,
        user_team_role_repository: UserTeamRoleRepository,
    ) -> None:
        self._permission_repository = permission_repository
        self._user_team_role_repository = user_team_role_repository

    async def get_all_permissions(self) -> list[PermissionDto]:
        permissions = await self._permission_repository.find_all()
        return [PermissionDto.from_model(permission) for permission in permissions]

    async def validate_user_access_team_resource(
        self, *, user_id: UUID, team_id: UUID, permission_scope: str
    ) -> None:
        if not await self._user_team_role_repository.is_user_has_permission_in_team(
            user_id=user_id, team_id=team_id, permission_scope=permission_scope
        ):
            raise ResourceAccessDeniedException
