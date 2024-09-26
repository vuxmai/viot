from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.database.repository.pagination import Page
from app.module.auth.repository.user_repository import TeamMember
from app.module.team.service.member_service import MemberService


async def test_find_paging_members(
    member_service: MemberService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    items = [
        TeamMember(user=mock_user, role="Member", joined_at=datetime.now()),
        TeamMember(user=mock_user, role="Owner", joined_at=datetime.now()),
    ]
    mock_user_repository.find_paging_member_by_team_id.return_value = Page(
        items=items, total_items=20, page=0, page_size=20
    )

    # when
    result = await member_service.find_paging_members(
        page=0,
        page_size=20,
        sort_direction_joined_at="desc",
        team_id=uuid4(),
    )

    # then
    assert len(result.items) == 2
    assert result.items[0].id == mock_user.id
    assert result.total_items == 20
    assert result.page == 0
    assert result.page_size == 20
