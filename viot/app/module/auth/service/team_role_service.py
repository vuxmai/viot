from uuid import UUID

from injector import inject

from ..dto.role_dto import RoleCreateDto
from ..exception.permission_exception import PermissionNotFoundException
from ..exception.role_exception import RoleNameExistsInTeamException
from ..model.role import Role
from ..model.role_permission import RolePermission
from ..repository.permission_repository import PermissionRepository
from ..repository.role_permission_repository import RolePermissionRepository
from ..repository.role_repository import RoleRepository


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

    async def create_role(self, *, team_id: UUID, role_create_dto: RoleCreateDto):
        # 1. Check role name exists in team
        # 2. Create role
        # 3. Create role permissions

        if await self._role_repository.is_role_name_exists_in_team(
            team_id=team_id, role_name=role_create_dto.name
        ):
            raise RoleNameExistsInTeamException(role_name=role_create_dto.name)

        role = await self._role_repository.save(
            Role(
                team_id=team_id,
                name=role_create_dto.name,
                description=role_create_dto.description,
            )
        )

        for scope in role_create_dto.scopes:
            permission = self._permission_repository.find_permission_by_scope(scope)
            if permission is None:
                raise PermissionNotFoundException(permission_scope=scope)

            await self._role_permission_repository.save(
                RolePermission(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )
