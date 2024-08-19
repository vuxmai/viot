from unittest.mock import AsyncMock, call, patch

from app.module.team.service import TeamService


async def test_correctly_when_unique_slug(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    mock_team_repository.exists_by_slug.return_value = False

    slug = await team_service._generate_team_slug(name="Test team")  # type: ignore

    assert slug == "test-team"


async def test_correctly_when_non_unique_slug(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    mock_team_repository.exists_by_slug.side_effect = [True, True, False]

    with patch("app.module.team.service.generate_random_string", return_value="1234"):
        slug = await team_service._generate_team_slug(name="Test team")  # type: ignore

    assert slug == "test-team-1234"
    assert mock_team_repository.exists_by_slug.call_count == 3
    assert mock_team_repository.exists_by_slug.call_args_list == [
        call("test-team"),
        call("test-team-1234"),
        call("test-team-1234"),
    ]
