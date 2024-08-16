from uuid import UUID

from injector import inject
from slugify import slugify

from .constant import TeamRole
from .dto import TeamCreateDto, TeamDto, TeamUpdateDto, TeamWithRoleDto
from .exception import TeamNotFoundException, TeamSlugAlreadyExistsException
from .model import Team, UserTeam
from .repository import TeamRepository, UserTeamRepository
from .utils import generate_random_string


class TeamService:
    @inject
    def __init__(self, team_repository: TeamRepository, user_team_repository: UserTeamRepository):
        self._team_repository = team_repository
        self._user_team_repository = user_team_repository

    async def get_teams_with_role_by_user_id(self, *, user_id: UUID) -> list[TeamWithRoleDto]:
        teams_with_roles = await self._team_repository.find_teams_with_role_by_user_id(user_id)
        return [TeamWithRoleDto.from_model(row.team, row.role) for row in teams_with_roles]

    async def _generate_team_slug(self, *, name: str) -> str:
        slug = slugify(name, separator="-")
        if await self._team_repository.exists_by_slug(slug):
            while True:
                new_slug = f"{slug}-{generate_random_string(6)}"
                if not await self._team_repository.exists_by_slug(new_slug):
                    return new_slug
        return slug

    async def create_team(self, *, user_id: UUID, team_create_dto: TeamCreateDto) -> TeamDto:
        default = not await self._team_repository.user_has_teams(user_id)
        slug = await self._generate_team_slug(name=team_create_dto.name)

        team = Team(
            owner_id=user_id,
            name=team_create_dto.name,
            slug=slug,
            description=team_create_dto.description,
            default=default,
        )

        team = await self._team_repository.save(team)
        await self._user_team_repository.save(
            UserTeam(user_id=user_id, team_id=team.id, role=TeamRole.OWNER)
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

    async def delete_team(self, *, team_id: UUID) -> None:
        team = await self._team_repository.find(team_id)
        if not team:
            raise TeamNotFoundException

        await self._team_repository.delete(team)
