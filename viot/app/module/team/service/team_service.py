import logging
from uuid import UUID

from injector import inject
from slugify import slugify

from app.module.auth.constants import TEAM_ROLE_OWNER, TEAM_ROLE_OWNER_DESCRIPTION
from app.module.auth.dto.role_dto import RoleCreateDto
from app.module.auth.model.user_team_role import UserTeamRole
from app.module.auth.repository.permission_repository import PermissionRepository
from app.module.auth.repository.user_team_role_repository import UserTeamRoleRepository
from app.module.auth.service.team_role_service import TeamRoleService

from ..dto.team_dto import TeamCreateDto, TeamDto, TeamUpdateDto, TeamWithRoleAndPermissionsDto
from ..exception.team_exception import TeamNotFoundException, TeamSlugAlreadyExistsException
from ..model.team import Team
from ..repository.team_repository import TeamRepository
from ..utils.slug_utils import generate_random_string

logger = logging.getLogger(__name__)


class TeamService:
    @inject
    def __init__(
        self,
        team_repository: TeamRepository,
        team_role_service: TeamRoleService,
        permission_repository: PermissionRepository,
        user_team_role_repository: UserTeamRoleRepository,
    ) -> None:
        self._team_repository = team_repository
        self._team_role_service = team_role_service
        self._permission_repository = permission_repository
        self._user_team_role_repository = user_team_role_repository

    async def get_teams_with_role_by_user_id(
        self, *, user_id: UUID
    ) -> list[TeamWithRoleAndPermissionsDto]:
        teams_with_roles = await self._team_repository.find_teams_with_role_by_user_id(user_id)
        return [
            TeamWithRoleAndPermissionsDto.from_model(
                row.team, row.role, permissions=row.permissions
            )
            for row in teams_with_roles
        ]

    async def _generate_team_slug(self, *, name: str) -> str:
        slug = slugify(name, separator="-")
        if await self._team_repository.exists_by_slug(slug):
            while True:
                new_slug = f"{slug}-{generate_random_string(6)}"
                if not await self._team_repository.exists_by_slug(new_slug):
                    return new_slug
        return slug

    async def create_team(self, *, user_id: UUID, team_create_dto: TeamCreateDto) -> TeamDto:
        logger.info(f"Creating team for user_id: {user_id}, request: {team_create_dto}")
        default = not await self._team_repository.user_has_teams(user_id)
        slug = await self._generate_team_slug(name=team_create_dto.name)

        # Create Team
        team = Team(
            name=team_create_dto.name,
            slug=slug,
            description=team_create_dto.description,
            default=default,
        )
        team = await self._team_repository.save(team)

        # Create Owner Role
        permissions = await self._permission_repository.find_all()
        role_dto = await self._team_role_service.create_role(
            team_id=team.id,
            role_create_dto=RoleCreateDto(
                name=TEAM_ROLE_OWNER,
                description=TEAM_ROLE_OWNER_DESCRIPTION,
                scopes={permission.scope for permission in permissions},
            ),
        )

        # Assign Owner Role to current user
        await self._user_team_role_repository.save(
            UserTeamRole(user_id=user_id, team_id=team.id, role_id=role_dto.id)
        )
        return TeamDto.from_model(team)

    async def update_team(self, *, team_id: UUID, team_update_dto: TeamUpdateDto) -> TeamDto:
        team = await self._team_repository.find(team_id)

        if not team:
            raise TeamNotFoundException

        if team_update_dto.slug and team_update_dto.slug != team.slug:
            if await self._team_repository.exists_by_slug(team_update_dto.slug):
                raise TeamSlugAlreadyExistsException

        for k, v in team_update_dto.model_dump(exclude_unset=True).items():
            setattr(team, k, v)

        team = await self._team_repository.save(team)
        return TeamDto.from_model(team)

    async def delete_team_by_id(self, *, team_id: UUID) -> None:
        await self._team_repository.delete_by_id(team_id)

    async def delete_all_teams_by_user_id(self, *, user_id: UUID) -> None:
        await self._team_repository.delete_all_by_user_id(user_id)
