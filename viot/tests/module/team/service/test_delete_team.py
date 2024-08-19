from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.team.exception import TeamNotFoundException
from app.module.team.service import TeamService


async def test_correctly(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock
) -> None:
    mock_team_repository.find.return_value = mock_team
    mock_team_repository.delete.return_value = None

    await team_service.delete_team(team_id=mock_team.id)

    mock_team_repository.find.assert_called_once_with(mock_team.id)
    mock_team_repository.delete.assert_called_once_with(mock_team)


async def test_raises_when_team_not_found(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    team_id = uuid4()
    mock_team_repository.find.return_value = None

    with pytest.raises(TeamNotFoundException):
        await team_service.delete_team(team_id=team_id)

    mock_team_repository.find.assert_called_once_with(team_id)
