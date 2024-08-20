from unittest.mock import AsyncMock, Mock

import pytest

from app.module.team_invitation.exception import TeamInvitationNotFoundException
from app.module.team_invitation.service import TeamInvitationService


async def test_correctly(
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


async def test_raises_when_invitation_not_found(
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
