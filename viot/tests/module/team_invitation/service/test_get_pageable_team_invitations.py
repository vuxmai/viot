from unittest.mock import AsyncMock, Mock

from app.database.repository import Page
from app.module.team_invitation.service import TeamInvitationService


async def test_correctly_with_empty_list(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_all_with_paging.return_value = Page(
        items=[],  # type: ignore
        total_items=0,
        page=0,
        page_size=0,
    )

    # when
    result = await team_invitation_service.get_pageable_team_invitations(
        team_id=mock_team_invitation.team_id,
        page=0,
        page_size=0,
    )

    # then
    assert result.items == []
    assert result.total_items == 0
    assert result.page == 0
    assert result.page_size == 0


async def test_correctly_with_10_items(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_all_with_paging.return_value = Page(
        items=[mock_team_invitation] * 10,  # type: ignore
        total_items=10,
        page=0,
        page_size=10,
    )

    # when
    result = await team_invitation_service.get_pageable_team_invitations(
        team_id=mock_team_invitation.team_id,
        page=0,
        page_size=10,
    )

    # then
    assert len(result.items) == 10
    assert result.total_items == 10
    assert result.page == 0
    assert result.page_size == 10
