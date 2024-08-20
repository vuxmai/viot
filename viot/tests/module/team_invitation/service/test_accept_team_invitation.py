from unittest.mock import AsyncMock, Mock

import pytest

from app.module.team_invitation.exception import TeamInvitationNotFoundException
from app.module.team_invitation.service import TeamInvitationService


async def test_correctly(
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


async def test_raises_when_invitation_not_found(
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


async def test_raises_when_invitee_not_found(
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
