from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from app.module.auth.dto.role_dto import RoleCreateDto
from app.module.auth.exception.permission_exception import PermissionsNotFoundException
from app.module.auth.exception.role_exception import RoleNameExistsInTeamException
from app.module.auth.model.permission import Permission
from app.module.auth.model.role import Role
from app.module.auth.service.team_role_service import TeamRoleService


@pytest.fixture
def mock_role_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_permission_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_role_permission_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def team_role_service(
    mock_role_repository: AsyncMock,
    mock_permission_repository: AsyncMock,
    mock_role_permission_repository: AsyncMock,
) -> TeamRoleService:
    return TeamRoleService(
        role_repository=mock_role_repository,
        permission_repository=mock_permission_repository,
        role_permission_repository=mock_role_permission_repository,
    )


@pytest.fixture
def mock_role() -> Mock:
    role = Mock(spec=Role)
    role.id = 1
    role.name = "test"
    role.description = "test"
    role.scopes = {"test"}
    role.created_at = datetime.now(UTC)
    role.updated_at = None
    return role


@pytest.fixture
def mock_permission() -> Mock:
    permission = Mock(spec=Permission)
    permission.id = 1
    permission.scope = "test"
    return permission


async def test_create_role(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
    mock_role: Mock,
    mock_permission: Mock,
) -> None:
    # given
    mock_role_repository.is_role_name_exists_in_team.return_value = False
    mock_role_repository.save.return_value = mock_role
    role_create_dto = RoleCreateDto(name="test", description="test", scopes={"test"})

    # when
    with patch.object(
        TeamRoleService, "validate_permission_exists"
    ) as mock_validate_permission_exists:
        mock_validate_permission_exists.return_value = [mock_permission]
        result = await team_role_service.create_role(
            team_id=uuid4(), role_create_dto=role_create_dto
        )

    # then
    assert result.name == mock_role.name
    assert result.description == mock_role.description
    assert result.scopes == mock_role.scopes


async def test_create_role_raise_role_name_exists_in_team(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
    mock_role: Mock,
    mock_permission: Mock,
) -> None:
    # given
    mock_role_repository.is_role_name_exists_in_team.return_value = True

    # when
    with pytest.raises(RoleNameExistsInTeamException):
        await team_role_service.create_role(
            team_id=uuid4(),
            role_create_dto=RoleCreateDto(name="test", description="test", scopes={"test"}),
        )


async def test_validate_permission_exists(
    team_role_service: TeamRoleService,
    mock_permission_repository: AsyncMock,
    mock_permission: Mock,
) -> None:
    # given
    mock_permission_repository.find_permissions_by_scopes.return_value = [mock_permission]

    # when
    result = await team_role_service.validate_permission_exists(scopes={"test"})

    # then
    assert result == [mock_permission]


async def test_validate_permission_exists_raise_permissions_not_found(
    team_role_service: TeamRoleService,
    mock_permission_repository: AsyncMock,
) -> None:
    # given
    mock_permission_repository.find_permissions_by_scopes.return_value = []

    # when
    with pytest.raises(PermissionsNotFoundException):
        await team_role_service.validate_permission_exists(scopes={"test"})
