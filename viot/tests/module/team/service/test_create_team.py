from unittest.mock import AsyncMock, Mock, patch

from app.module.team.dto import TeamCreateDto
from app.module.team.service import TeamService


async def test_correctly_when_create_default_team(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock, mock_user: Mock
) -> None:
    mock_team_repository.user_has_teams.return_value = False
    with patch.object(TeamService, "_generate_team_slug", return_value="test-team"):
        mock_team.name = "Test team"
        mock_team.slug = "test-team"
        mock_team.description = "Test description"
        mock_team.default = True
        mock_team_repository.save.return_value = mock_team

        team = await team_service.create_team(
            user_id=mock_user.id,
            team_create_dto=TeamCreateDto(name="Test team", description="Test description"),
        )

    assert team.name == "Test team"
    assert team.slug == "test-team"
    assert team.description == "Test description"
    assert team.default is True


async def test_correctly_when_create_non_default_team(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock, mock_user: Mock
) -> None:
    mock_team_repository.user_has_teams.return_value = True
    with patch.object(TeamService, "_generate_team_slug", return_value="test-team"):
        mock_team.name = "Test team"
        mock_team.slug = "test-team"
        mock_team.description = "Test description"
        mock_team.default = False
        mock_team_repository.save.return_value = mock_team

        team = await team_service.create_team(
            user_id=mock_user.id,
            team_create_dto=TeamCreateDto(name="Test team", description="Test description"),
        )

    assert team.name == "Test team"
    assert team.slug == "test-team"
    assert team.description == "Test description"
    assert team.default is False
