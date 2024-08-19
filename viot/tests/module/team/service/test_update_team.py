from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.team.dto import TeamUpdateDto
from app.module.team.exception import TeamNotFoundException, TeamSlugAlreadyExistsException
from app.module.team.service import TeamService


async def test_correctly(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock
) -> None:
    mock_team_repository.find.return_value = mock_team
    mock_team_repository.exists_by_slug.return_value = False
    mock_team_repository.save.return_value = mock_team

    update_dto = TeamUpdateDto(
        name="Updated Team", slug="updated-slug", description="Updated description"
    )
    result = await team_service.update_team(team_id=mock_team.id, team_update_dto=update_dto)

    mock_team_repository.find.assert_called_once_with(mock_team.id)
    mock_team_repository.exists_by_slug.assert_called_once_with("updated-slug")
    mock_team_repository.save.assert_called_once_with(mock_team)

    assert result.name == "Updated Team"
    assert result.slug == "updated-slug"
    assert result.description == "Updated description"


async def test_raises_when_team_not_found(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    team_id = uuid4()
    mock_team_repository.find.return_value = None

    update_dto = TeamUpdateDto(name="Updated Team")
    with pytest.raises(TeamNotFoundException):
        await team_service.update_team(team_id=team_id, team_update_dto=update_dto)

    mock_team_repository.find.assert_called_once_with(team_id)


async def test_raises_when_slug_already_exists(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock
) -> None:
    team_id = uuid4()
    mock_team_repository.find.return_value = mock_team
    mock_team_repository.exists_by_slug.return_value = True

    update_dto = TeamUpdateDto(slug="existing-slug")
    with pytest.raises(TeamSlugAlreadyExistsException):
        await team_service.update_team(team_id=team_id, team_update_dto=update_dto)

    mock_team_repository.find.assert_called_once_with(team_id)
    mock_team_repository.exists_by_slug.assert_called_once_with("existing-slug")
