from unittest.mock import AsyncMock, Mock

import pytest

from app.database.repository import Page
from app.module.auth.exception.user_exception import UserNotFoundException
from app.module.team.constants import TeamRole
from app.module.team.dto.team_invitation_dto import TeamInvitationCreateDto
from app.module.team.exception.team_exception import TeamNotFoundException
from app.module.team.exception.team_invitation_exception import TeamInvitationNotFoundException
from app.module.team.service.team_invitation_service import TeamInvitationService


async def test_get_pageable_team_invitations_correctly_with_empty_list(
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


async def test_get_pageable_team_invitations_correctly_with_10_items(
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


async def test_create_team_invitation_correctly(
    team_invitation_service: TeamInvitationService,
    mock_email_service: Mock,
    mock_team_invitation_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
    mock_user: Mock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = mock_user
    mock_team_repository.find.return_value = mock_team
    mock_team_invitation_repository.save.return_value = mock_team_invitation
    mock_email_service.send_team_invitation_email.return_value = None

    # when
    team_invitation_create_dto = TeamInvitationCreateDto(
        email="test@example.com",
        role=TeamRole.MEMBER,
    )
    await team_invitation_service.create_team_invitation(
        team_id=mock_team.id,
        inviter=mock_user,
        team_invitation_create_dto=team_invitation_create_dto,
    )

    # then
    mock_user_repository.find_by_email.assert_called_once_with(team_invitation_create_dto.email)
    mock_team_repository.find.assert_called_once_with(mock_team.id)
    mock_team_invitation_repository.save.assert_called_once()
    mock_email_service.send_team_invitation_email.assert_called_once()


async def test_create_team_invitation_raises_when_invitee_not_found(
    team_invitation_service: TeamInvitationService,
    mock_email_service: Mock,
    mock_team_invitation_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_team_repository: AsyncMock,
    mock_user: Mock,
    mock_team: Mock,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = None

    # when
    team_invitation_create_dto = TeamInvitationCreateDto(
        email="test@example.com",
        role=TeamRole.MEMBER,
    )
    with pytest.raises(UserNotFoundException):
        await team_invitation_service.create_team_invitation(
            team_id=mock_team.id,
            inviter=mock_user,
            team_invitation_create_dto=team_invitation_create_dto,
        )

    # then
    mock_user_repository.find_by_email.assert_called_once_with(team_invitation_create_dto.email)
    mock_team_repository.find.assert_not_called()
    mock_team_invitation_repository.save.assert_not_called()
    mock_email_service.send_team_invitation_email.assert_not_called()


async def test_create_team_invitation_raises_when_team_not_found(
    team_invitation_service: TeamInvitationService,
    mock_email_service: Mock,
    mock_team_invitation_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_team_repository: AsyncMock,
    mock_user: Mock,
    mock_team: Mock,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = mock_user
    mock_team_repository.find.return_value = None

    # when
    team_invitation_create_dto = TeamInvitationCreateDto(
        email="test@example.com",
        role=TeamRole.MEMBER,
    )
    with pytest.raises(TeamNotFoundException):
        await team_invitation_service.create_team_invitation(
            team_id=mock_team.id,
            inviter=mock_user,
            team_invitation_create_dto=team_invitation_create_dto,
        )

    # then
    mock_user_repository.find_by_email.assert_called_once_with(team_invitation_create_dto.email)
    mock_team_repository.find.assert_called_once_with(mock_team.id)
    mock_team_invitation_repository.save.assert_not_called()
    mock_email_service.send_team_invitation_email.assert_not_called()


async def test_accept_team_invitation_correctly(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_user_team_repository: AsyncMock,
    mock_team: Mock,
    mock_user: Mock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_by_token.return_value = mock_team_invitation
    mock_user_repository.find_id_by_email.return_value = mock_user.id
    mock_user_team_repository.save.return_value = None

    # when
    await team_invitation_service.accept_team_invitation(token=mock_team_invitation.token)

    # then
    mock_team_invitation_repository.find_by_token.assert_called_once_with(
        mock_team_invitation.token
    )
    mock_user_repository.find_id_by_email.assert_called_once_with(mock_team_invitation.email)
    mock_user_team_repository.save.assert_called_once()
    mock_team_invitation_repository.delete.assert_called_once_with(mock_team_invitation)


async def test_accept_team_invitation_raises_when_invitation_not_found(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_user_team_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_by_token.return_value = None

    # when
    with pytest.raises(TeamInvitationNotFoundException):
        await team_invitation_service.accept_team_invitation(token=mock_team_invitation.token)

    # then
    mock_team_invitation_repository.find_by_token.assert_called_once_with(
        mock_team_invitation.token
    )
    mock_user_repository.find_id_by_email.assert_not_called()
    mock_user_team_repository.save.assert_not_called()
    mock_team_invitation_repository.delete.assert_not_called()


async def test_accept_team_invitation_raises_when_invitee_not_found(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_user_team_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_by_token.return_value = mock_team_invitation
    mock_user_repository.find_id_by_email.return_value = None

    # when
    await team_invitation_service.accept_team_invitation(token=mock_team_invitation.token)

    # then
    mock_team_invitation_repository.find_by_token.assert_called_once_with(
        mock_team_invitation.token
    )
    mock_user_repository.find_id_by_email.assert_called_once_with(mock_team_invitation.email)
    mock_user_team_repository.save.assert_not_called()
    mock_team_invitation_repository.delete.assert_called_once_with(mock_team_invitation)


async def test_decline_team_invitation_by_token_correctly(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_by_token.return_value = mock_team_invitation

    # when
    await team_invitation_service._delete_team_invitation_by_token(mock_team_invitation.token)  # type: ignore

    # then
    mock_team_invitation_repository.find_by_token.assert_called_once_with(
        mock_team_invitation.token
    )
    mock_team_invitation_repository.delete.assert_called_once_with(mock_team_invitation)


async def test_decline_team_invitation_by_token_raises_when_invitation_not_found(
    team_invitation_service: TeamInvitationService,
    mock_team_invitation_repository: AsyncMock,
    mock_team_invitation: Mock,
) -> None:
    # given
    mock_team_invitation_repository.find_by_token.return_value = None

    # when
    with pytest.raises(TeamInvitationNotFoundException):
        await team_invitation_service._delete_team_invitation_by_token(mock_team_invitation.token)  # type: ignore

    # then
    mock_team_invitation_repository.find_by_token.assert_called_once_with(
        mock_team_invitation.token
    )
    mock_team_invitation_repository.delete.assert_not_called()
