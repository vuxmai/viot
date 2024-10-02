import logging
from typing import cast
from uuid import UUID

from injector import inject

from app.module.team.exception.team_exception import TeamNotFoundException
from app.module.team.repository.team_repository import TeamRepository

from ..constants import MAX_ROLES_PER_TEAM, SENSITIVE_SCOPES, TEAM_ROLE_OWNER
from ..dto.role_dto import RoleCreateDto, RoleDto, RoleUpdateDto
from ..exception.permission_exception import (
    PermissionsNotFoundException,
    UpdateSensitiveScopeException,
)
from ..exception.role_exception import (
    CannotModifyOwnerRoleException,
    RoleIdNotFoundException,
    RoleNameExistsInTeamException,
    TeamRoleLimitException,
)
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
        team_repository: TeamRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
    ) -> None:
        self._role_repository = role_repository
        self._team_repository = team_repository
        self._permission_repository = permission_repository
        self._role_permission_repository = role_permission_repository

    async def get_roles_by_team_id(self, *, team_id: UUID) -> list[RoleDto]:
        if not await self._team_repository.exists_by_id(team_id):
            raise TeamNotFoundException
        results = await self._role_repository.find_all_by_team_id(team_id=team_id)
        return [RoleDto.from_model(r.role, r.scopes) for r in results]

    async def create_role(self, *, team_id: UUID, role_create_dto: RoleCreateDto) -> RoleDto:
        await self.validate_team_roles_limit(team_id=team_id)
        await self.validate_role_name_not_exists_in_team(
            team_id=team_id, role_name=role_create_dto.name
        )
        permissions = await self.validate_permission_exists(role_create_dto.scopes)

        role = await self._role_repository.save(
            Role(
                team_id=team_id, name=role_create_dto.name, description=role_create_dto.description
            )
        )

        await self._role_permission_repository.bulk_save(
            [{"role_id": role.id, "permission_id": permission.id} for permission in permissions]
        )

        return RoleDto.from_model(role, role_create_dto.scopes)

    async def validate_role_name_not_exists_in_team(self, *, team_id: UUID, role_name: str) -> None:
        if await self._role_repository.is_role_name_exists_in_team(
            team_id=team_id, role_name=role_name
        ):
            raise RoleNameExistsInTeamException(role_name=role_name)

    async def validate_permission_exists(self, scopes: set[str]) -> list[Permission]:
        logger.debug(f"Validating permissions: {scopes}")
        if not scopes:
            return []

        permissions = await self._permission_repository.find_by_scopes(scopes)
        if len(permissions) == len(scopes):
            return cast(list[Permission], permissions)

        in_db_scopes = {permission.scope for permission in permissions}
        missing_permissions = [scope for scope in scopes if scope not in in_db_scopes]
        raise PermissionsNotFoundException(missing_permissions)

    async def validate_team_roles_limit(self, team_id: UUID) -> None:
        if await self._role_repository.count_by_team_id(team_id=team_id) >= MAX_ROLES_PER_TEAM:
            raise TeamRoleLimitException(team_id=team_id)

    async def validate_not_modify_owner_role(self, role_id: int) -> None:
        role_name = await self._role_repository.find_role_name_by_id(role_id=role_id)
        if role_name == TEAM_ROLE_OWNER:
            raise CannotModifyOwnerRoleException

    def validate_not_update_sensitive_permissions(self, scopes: set[str]) -> None:
        if any(s in scopes for s in SENSITIVE_SCOPES):
            raise UpdateSensitiveScopeException

    async def update_role(
        self, *, role_id: int, team_id: UUID, role_update_dto: RoleUpdateDto
    ) -> RoleDto:
        await self.validate_not_modify_owner_role(role_id=role_id)

        role = await self._role_repository.find(role_id)
        if role is None:
            raise RoleIdNotFoundException(role_id=role_id)
        if role.name != role_update_dto.name:
            await self.validate_role_name_not_exists_in_team(
                team_id=team_id, role_name=role_update_dto.name
            )

        self.validate_not_update_sensitive_permissions(role_update_dto.scopes)
        permissions = await self.validate_permission_exists(role_update_dto.scopes)

        role.name = role_update_dto.name
        role.description = role_update_dto.description
        await self._role_repository.save(role)

        if permissions:
            await self._role_permission_repository.bulk_save_on_conflict_do_nothing(
                [{"role_id": role.id, "permission_id": permission.id} for permission in permissions]
            )

        return RoleDto.from_model(role, role_update_dto.scopes)

    async def delete_role(self, *, role_id: int, team_id: UUID) -> None:
        await self.validate_not_modify_owner_role(role_id=role_id)
        await self._role_repository.delete_by_id_and_team_id(role_id=role_id, team_id=team_id)
