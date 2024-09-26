from datetime import datetime
from uuid import UUID

from app.common.dto import BaseOutDto, PagingDto
from app.database.repository.pagination import Page
from app.module.auth.repository.user_repository import TeamMember


class MemberDto(BaseOutDto):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: str
    joined_at: datetime

    @classmethod
    def from_model(cls, user: TeamMember) -> "MemberDto":
        return MemberDto(
            id=user.user.id,
            first_name=user.user.first_name,
            last_name=user.user.last_name,
            email=user.user.email,
            role=user.role,
            joined_at=user.joined_at,
        )


class MemberPagingDto(PagingDto[MemberDto]):
    @classmethod
    def from_page(cls, page: Page[TeamMember]) -> "MemberPagingDto":
        return MemberPagingDto(
            items=[MemberDto.from_model(user) for user in page.items],
            total_items=page.total_items,
            page=page.page,
            page_size=page.page_size,
        )
