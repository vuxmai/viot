from uuid import UUID

from injector import inject

from app.database.repository import Pageable, Sort
from app.database.repository.pagination import SortDirection
from app.module.auth.model.user_team_role import UserTeamRole
from app.module.auth.repository.user_repository import UserRepository

from ..dto.member_dto import MemberPagingDto


class MemberService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

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
