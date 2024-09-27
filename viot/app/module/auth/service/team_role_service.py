import logging
from typing import cast
from uuid import UUID

from injector import inject

from ..dto.role_dto import RoleCreateDto, RoleDto
from ..exception.permission_exception import PermissionsNotFoundException
from ..exception.role_exception import RoleNameExistsInTeamException
from ..model.permission import Permission
from ..model.role import Role
from ..repository.permission_repository import PermissionRepository
from ..repository.role_permission_repository import RolePermissionRepository
from ..repository.role_repository import RoleRepository

logger = logging.getLogger(__name__)


class TeamRoleService:
    @inject
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
    ) -> None:
        self._role_repository = role_repository
        self._permission_repository = permission_repository
        self._role_permission_repository = role_permission_repository

    async def create_role(self, *, team_id: UUID, role_create_dto: RoleCreateDto) -> RoleDto:
        if await self._role_repository.is_role_name_exists_in_team(
            team_id=team_id, role_name=role_create_dto.name
        ):
            raise RoleNameExistsInTeamException(role_name=role_create_dto.name)

        role = await self._role_repository.save(
            Role(
                team_id=team_id, name=role_create_dto.name, description=role_create_dto.description
            )
        )

        permissions = await self.validate_permission_exists(role_create_dto.scopes)

        await self._role_permission_repository.bulk_save(
            [
                {
                    "role_id": role.id,
                    "permission_id": permission.id,
                }
                for permission in permissions
            ]
        )

        return RoleDto(**role.to_dict(), scopes=role_create_dto.scopes)

    async def validate_permission_exists(self, scopes: set[str]) -> list[Permission]:
        logger.debug(f"Validating permissions: {scopes}")
        permissions = await self._permission_repository.find_permissions_by_scopes(scopes)
        if len(permissions) == len(scopes):
            return cast(list[Permission], permissions)

        in_db_scopes = {permission.scope for permission in permissions}
        missing_permissions = [scope for scope in scopes if scope not in in_db_scopes]
        raise PermissionsNotFoundException(missing_permissions)
