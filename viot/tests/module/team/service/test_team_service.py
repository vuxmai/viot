from unittest.mock import AsyncMock, Mock, call, patch
from uuid import uuid4

import pytest

from app.module.team.dto.team_dto import TeamCreateDto, TeamUpdateDto
from app.module.team.exception.team_exception import (
    TeamNotFoundException,
    TeamSlugAlreadyExistsException,
)
from app.module.team.repository.team_repository import TeamWithRoleAndPermissions
from app.module.team.service.team_service import TeamService


@pytest.fixture
def mock_team_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_team_role_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_permission_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_user_team_role_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def team_service(
    mock_team_repository: AsyncMock,
    mock_permission_repository: AsyncMock,
    mock_user_team_role_repository: AsyncMock,
    mock_team_role_service: AsyncMock,
) -> TeamService:
    return TeamService(
        team_repository=mock_team_repository,
        team_role_service=mock_team_role_service,
        permission_repository=mock_permission_repository,
        user_team_role_repository=mock_user_team_role_repository,
    )


async def test_get_teams_with_role_by_user_id_when_get_one_team(
    team_service: TeamService,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
) -> None:
    mock = Mock(spec=TeamWithRoleAndPermissions)
    mock.team = mock_team
    mock.role = "Test role"
    mock.permissions = set()
    mock_team_repository.find_teams_with_role_by_user_id.return_value = [mock]

    result = await team_service.get_teams_with_role_by_user_id(user_id=uuid4())

    assert len(result) == 1
    assert result[0].name == mock_team.name
    assert result[0].description == mock_team.description
    assert result[0].role == "Test role"
    assert result[0].permissions == set()


async def test_get_teams_with_role_by_user_id_when_get_3_teams(
    team_service: TeamService,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
) -> None:
    mocks: list[Mock] = []
    for i in range(3):
        mock = Mock(spec=TeamWithRoleAndPermissions)
        mock.team = mock_team
        mock.role = f"Role {i+1}"
        mock.permissions = set()
        mocks.append(mock)
    mock_team_repository.find_teams_with_role_by_user_id.return_value = mocks

    result = await team_service.get_teams_with_role_by_user_id(user_id=uuid4())

    assert len(result) == 3
    assert result[0].name == mock_team.name
    assert result[0].description == mock_team.description
    assert result[0].role == "Role 1"
    assert result[0].permissions == set()
    assert result[1].name == mock_team.name
    assert result[1].description == mock_team.description
    assert result[1].role == "Role 2"
    assert result[1].permissions == set()
    assert result[2].name == mock_team.name
    assert result[2].description == mock_team.description


async def test_generate_team_slug_correctly_when_unique_slug(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    mock_team_repository.exists_by_slug.return_value = False

    slug = await team_service._generate_team_slug(name="Test team")  # type: ignore

    assert slug == "test-team"


async def test_generate_team_slug_correctly_when_non_unique_slug(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    mock_team_repository.exists_by_slug.side_effect = [True, True, False]

    with patch("app.module.team.service.team_service.generate_random_string", return_value="1234"):
        slug = await team_service._generate_team_slug(name="Test team")  # type: ignore

    assert slug == "test-team-1234"
    assert mock_team_repository.exists_by_slug.call_count == 3
    assert mock_team_repository.exists_by_slug.call_args_list == [
        call("test-team"),
        call("test-team-1234"),
        call("test-team-1234"),
    ]


async def test_create_team_correctly_when_create_default_team(
    team_service: TeamService,
    mock_team_repository: AsyncMock,
    mock_team: Mock,
    mock_user: Mock,
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


async def test_create_team_correctly_when_create_non_default_team(
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


async def test_update_team_correctly(
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


async def test_update_team_correctly_when_team_not_found(
    team_service: TeamService, mock_team_repository: AsyncMock
) -> None:
    team_id = uuid4()
    mock_team_repository.find.return_value = None

    update_dto = TeamUpdateDto(name="Updated Team")
    with pytest.raises(TeamNotFoundException):
        await team_service.update_team(team_id=team_id, team_update_dto=update_dto)

    mock_team_repository.find.assert_called_once_with(team_id)


async def test_update_team_correctly_when_slug_already_exists(
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


async def test_delete_team_correctly(
    team_service: TeamService, mock_team_repository: AsyncMock, mock_team: Mock
) -> None:
    await team_service.delete_team_by_id(team_id=mock_team.id)

    mock_team_repository.delete_by_id.assert_called_once_with(mock_team.id)
