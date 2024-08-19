from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.module.team.projection import TeamWithRole
from app.module.team.service import TeamService


async def test_correctly_when_get_one_team(
    team_service: TeamService,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
) -> None:
    mock_team_with_role = Mock(spec=TeamWithRole)
    mock_team_with_role.team = mock_team
    mock_team_with_role.role = "Test role"
    mock_team_repository.find_teams_with_role_by_user_id.return_value = [mock_team_with_role]

    teams_with_role = await team_service.get_teams_with_role_by_user_id(user_id=uuid4())

    assert len(teams_with_role) == 1
    assert teams_with_role[0].name == mock_team.name
    assert teams_with_role[0].description == mock_team.description
    assert teams_with_role[0].role == "Test role"


async def test_correctly_when_get_3_teams(
    team_service: TeamService,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
) -> None:
    mock_teams_with_roles: list[Mock] = []
    for i in range(3):
        mock_team_with_role = Mock(spec=TeamWithRole)
        mock_team_with_role.team = mock_team
        mock_team_with_role.role = f"Role {i+1}"
        mock_teams_with_roles.append(mock_team_with_role)
    mock_team_repository.find_teams_with_role_by_user_id.return_value = mock_teams_with_roles

    teams_with_role = await team_service.get_teams_with_role_by_user_id(user_id=uuid4())

    assert len(teams_with_role) == 3
    assert teams_with_role[0].name == mock_team.name
    assert teams_with_role[0].description == mock_team.description
    assert teams_with_role[0].role == "Role 1"
    assert teams_with_role[1].name == mock_team.name
    assert teams_with_role[1].description == mock_team.description
    assert teams_with_role[1].role == "Role 2"
    assert teams_with_role[2].name == mock_team.name
    assert teams_with_role[2].description == mock_team.description
