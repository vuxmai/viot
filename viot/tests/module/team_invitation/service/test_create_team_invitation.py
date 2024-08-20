from unittest.mock import AsyncMock, Mock

import pytest

from app.module.team.constant import TeamRole
from app.module.team.exception import TeamNotFoundException
from app.module.team_invitation.dto import TeamInvitationCreateDto
from app.module.team_invitation.service import TeamInvitationService
from app.module.user.exception import UserNotFoundException


async def test_correctly(
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


async def test_raises_when_invitee_not_found(
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


async def test_raises_when_team_not_found(
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
