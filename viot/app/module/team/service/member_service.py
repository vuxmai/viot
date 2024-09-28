from uuid import UUID

from injector import inject

from app.database.repository import Pageable, Sort
from app.database.repository.pagination import SortDirection
from app.module.auth.exception.role_exception import RoleIdNotFoundException
from app.module.auth.exception.user_exception import UserNotFoundException
from app.module.auth.model.user_team_role import UserTeamRole
from app.module.auth.repository.role_repository import RoleRepository
from app.module.auth.repository.user_repository import TeamMember, UserRepository
from app.module.auth.repository.user_team_role_repository import UserTeamRoleRepository
from app.module.team.exception.member_exception import AssignSensitiveRoleException

from ..constants import TEAM_ROLE_OWNER
from ..dto.member_dto import MemberDto, MemberPagingDto, MemberUpdateDto


class MemberService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        user_team_role_repository: UserTeamRoleRepository,
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._user_team_role_repository = user_team_role_repository

    async def find_paging_members(
        self,
        *,
        page: int,
        page_size: int,
        sort_direction_joined_at: SortDirection,
        team_id: UUID,
    ) -> MemberPagingDto:
        member_page = await self._user_repository.find_paging_member_by_team_id(
            team_id,
            Pageable(
                page=page,
                page_size=page_size,
                sorts=[Sort(UserTeamRole.created_at, sort_direction_joined_at)],
            ),
        )
        return MemberPagingDto.from_page(member_page)

    async def _get_member_by_id_and_team_id(self, *, team_id: UUID, member_id: UUID) -> TeamMember:
        member = await self._user_repository.find_user_by_id_and_team_id(member_id, team_id)
        if member is None:
            raise UserNotFoundException
        return member

    async def get_member_by_id_and_team_id(self, *, team_id: UUID, member_id: UUID) -> MemberDto:
        member = await self._get_member_by_id_and_team_id(team_id=team_id, member_id=member_id)
        return MemberDto.from_model(member)

    async def update_member(
        self, *, team_id: UUID, member_id: UUID, member_update_dto: MemberUpdateDto
    ) -> MemberDto:
        member = await self._get_member_by_id_and_team_id(team_id=team_id, member_id=member_id)
        if member_update_dto.role_id is None:
            return MemberDto.from_model(member)

        # Find role name with role id and team id
        role_name = await self._role_repository.find_role_name_by_role_id_and_team_id(
            team_id=team_id, role_id=member_update_dto.role_id
        )
        if role_name is None:
            raise RoleIdNotFoundException(member_update_dto.role_id)

        # Check update old role
        if member.role == role_name:
            return MemberDto.from_model(member)

        # Check sensitive role
        self.validate_sensitive_role(role_name=role_name)

        # Update role id
        await self._user_team_role_repository.update_role_id(
            user_id=member_id, team_id=team_id, role_id=member_update_dto.role_id
        )

        member.role = role_name
        return MemberDto.from_model(member)

    async def delete_member(self, *, team_id: UUID, member_id: UUID) -> None:
        await self._user_repository.delete_user_by_id_and_team_id(member_id, team_id)

    def validate_sensitive_role(self, *, role_name: str) -> None:
        """Validate sensitive role"""
        if role_name in [TEAM_ROLE_OWNER]:
            raise AssignSensitiveRoleException(role_name)
