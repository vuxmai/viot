from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from app.module.auth.constants import SENSITIVE_SCOPES, TEAM_ROLE_OWNER
from app.module.auth.dto.role_dto import RoleCreateDto, RoleUpdateDto
from app.module.auth.exception.permission_exception import (
    PermissionsNotFoundException,
    UpdateSensitiveScopeException,
)
from app.module.auth.exception.role_exception import (
    CannotModifyOwnerRoleException,
    RoleIdNotFoundException,
    RoleNameExistsInTeamException,
    TeamRoleLimitException,
)
from app.module.auth.repository.role_repository import RoleWithScopes
from app.module.auth.service.team_role_service import TeamRoleService
from app.module.team.exception.team_exception import TeamNotFoundException


@pytest.fixture
def mock_role_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_team_repository() -> AsyncMock:
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
    mock_team_repository: AsyncMock,
    mock_permission_repository: AsyncMock,
    mock_role_permission_repository: AsyncMock,
) -> TeamRoleService:
    return TeamRoleService(
        role_repository=mock_role_repository,
        team_repository=mock_team_repository,
        permission_repository=mock_permission_repository,
        role_permission_repository=mock_role_permission_repository,
    )


async def test_get_roles_by_team_id(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
    mock_role: Mock,
) -> None:
    # given
    mock_role_repository.find_all_by_team_id.return_value = [
        RoleWithScopes(role=mock_role, scopes=mock_role.scopes)
    ]

    # when
    result = await team_role_service.get_roles_by_team_id(team_id=uuid4())

    # then
    assert result[0].name == mock_role.name
    assert result[0].description == mock_role.description
    assert result[0].scopes == mock_role.scopes


async def test_get_roles_by_team_id_raise_team_not_found(
    team_role_service: TeamRoleService,
    mock_team_repository: AsyncMock,
) -> None:
    # given
    mock_team_repository.exists_by_id.return_value = False

    # when
    with pytest.raises(TeamNotFoundException):
        await team_role_service.get_roles_by_team_id(team_id=uuid4())


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
    with (
        patch.object(TeamRoleService, "validate_team_roles_limit", return_value=None),
        patch.object(TeamRoleService, "validate_role_name_not_exists_in_team", return_value=None),
        patch.object(TeamRoleService, "validate_permission_exists", return_value=[mock_permission]),
    ):
        result = await team_role_service.create_role(
            team_id=uuid4(), role_create_dto=role_create_dto
        )

    # then
    assert result.name == mock_role.name
    assert result.description == mock_role.description
    assert result.scopes == mock_role.scopes


async def test_create_role_raise_team_role_limit(team_role_service: TeamRoleService) -> None:
    # when
    with patch.object(
        TeamRoleService, "validate_team_roles_limit", side_effect=TeamRoleLimitException(uuid4())
    ):
        with pytest.raises(TeamRoleLimitException):
            await team_role_service.create_role(
                team_id=uuid4(),
                role_create_dto=RoleCreateDto(name="test", description="test", scopes={"test"}),
            )


async def test_create_role_raise_role_name_exists_in_team(
    team_role_service: TeamRoleService,
) -> None:
    # when
    with (
        patch.object(TeamRoleService, "validate_team_roles_limit", return_value=None),
        patch.object(
            TeamRoleService,
            "validate_role_name_not_exists_in_team",
            side_effect=RoleNameExistsInTeamException("test"),
        ),
    ):
        with pytest.raises(RoleNameExistsInTeamException):
            await team_role_service.create_role(
                team_id=uuid4(),
                role_create_dto=RoleCreateDto(name="test", description="test", scopes={"test"}),
            )


async def test_create_role_raise_permission_not_found(
    team_role_service: TeamRoleService,
) -> None:
    # when
    with (
        patch.object(TeamRoleService, "validate_team_roles_limit", return_value=None),
        patch.object(TeamRoleService, "validate_role_name_not_exists_in_team", return_value=None),
        patch.object(
            TeamRoleService,
            "validate_permission_exists",
            side_effect=PermissionsNotFoundException(["test"]),
        ),
    ):
        with pytest.raises(PermissionsNotFoundException):
            await team_role_service.create_role(
                team_id=uuid4(),
                role_create_dto=RoleCreateDto(name="test", description="test", scopes={"test"}),
            )


async def test_validate_role_name_not_exists_in_team(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.is_role_name_exists_in_team.return_value = False

    # when
    await team_role_service.validate_role_name_not_exists_in_team(team_id=uuid4(), role_name="test")


async def test_validate_role_name_not_exists_in_team_raise_role_name_exists_in_team(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.is_role_name_exists_in_team.return_value = True

    # when
    with pytest.raises(RoleNameExistsInTeamException):
        await team_role_service.validate_role_name_not_exists_in_team(
            team_id=uuid4(), role_name="test"
        )


async def test_validate_permission_exists(
    team_role_service: TeamRoleService,
    mock_permission_repository: AsyncMock,
    mock_permission: Mock,
) -> None:
    # given
    mock_permission_repository.find_by_scopes.return_value = [mock_permission]

    # when
    result = await team_role_service.validate_permission_exists(scopes={"test"})

    # then
    assert result == [mock_permission]


async def test_validate_permission_exists_with_empty_scopes(
    team_role_service: TeamRoleService,
) -> None:
    # when
    result = await team_role_service.validate_permission_exists(scopes=set())

    # then
    assert result == []


async def test_validate_permission_exists_raise_permissions_not_found(
    team_role_service: TeamRoleService,
    mock_permission_repository: AsyncMock,
) -> None:
    # given
    mock_permission_repository.find_permissions_by_scopes.return_value = []

    # when
    with pytest.raises(PermissionsNotFoundException):
        await team_role_service.validate_permission_exists(scopes={"test"})


async def test_validate_team_roles_limit(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.count_by_team_id.return_value = 1

    # when
    await team_role_service.validate_team_roles_limit(team_id=uuid4())


async def test_validate_team_roles_limit_raise_team_role_limit(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.count_by_team_id.return_value = 5

    # when
    with pytest.raises(TeamRoleLimitException):
        await team_role_service.validate_team_roles_limit(team_id=uuid4())


async def test_validate_not_modify_owner_role(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.find_role_name_by_id.return_value = TEAM_ROLE_OWNER + "diff"

    # when
    await team_role_service.validate_not_modify_owner_role(role_id=1)


async def test_validate_not_modify_owner_role_raise_owner_role(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.find_role_name_by_id.return_value = TEAM_ROLE_OWNER

    # when
    with pytest.raises(CannotModifyOwnerRoleException):
        await team_role_service.validate_not_modify_owner_role(role_id=1)


async def test_validate_not_update_sensitive_permissions(
    team_role_service: TeamRoleService,
) -> None:
    # when
    team_role_service.validate_not_update_sensitive_permissions(scopes={"test"})


async def test_validate_not_update_sensitive_permissions_raise_sensitive_scope(
    team_role_service: TeamRoleService,
) -> None:
    # when
    with pytest.raises(UpdateSensitiveScopeException):
        team_role_service.validate_not_update_sensitive_permissions(
            scopes={list(SENSITIVE_SCOPES)[0]}
        )


async def test_update_role(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
    mock_permission: Mock,
    mock_role: Mock,
) -> None:
    # given
    mock_role_repository.find.return_value = mock_role
    mock_role_repository.find_role_name_by_id.return_value = "test"
    role_update_dto = Mock()
    role_update_dto.name = "test"
    role_update_dto.description = "test"
    role_update_dto.scopes = {"test"}

    # when
    with (
        patch.object(TeamRoleService, "validate_not_modify_owner_role", return_value=None),
        patch.object(TeamRoleService, "validate_role_name_not_exists_in_team", return_value=None),
        patch.object(TeamRoleService, "validate_permission_exists", return_value=[mock_permission]),
    ):
        result = await team_role_service.update_role(
            role_id=1, team_id=uuid4(), role_update_dto=role_update_dto
        )

    # then
    assert result.name == mock_role.name
    assert result.description == mock_role.description
    assert result.scopes == mock_role.scopes


async def test_update_role_raise_modify_owner_role(
    team_role_service: TeamRoleService,
) -> None:
    # when
    with patch.object(
        TeamRoleService,
        "validate_not_modify_owner_role",
        side_effect=CannotModifyOwnerRoleException,
    ):
        with pytest.raises(CannotModifyOwnerRoleException):
            await team_role_service.update_role(
                role_id=1,
                team_id=uuid4(),
                role_update_dto=RoleUpdateDto(name="test", description="test", scopes={"test"}),
            )


async def test_update_role_raise_role_id_not_found(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # given
    mock_role_repository.find.return_value = None

    # when
    with pytest.raises(RoleIdNotFoundException):
        await team_role_service.update_role(
            role_id=1,
            team_id=uuid4(),
            role_update_dto=RoleUpdateDto(name="test", description="test", scopes={"test"}),
        )


async def test_update_role_raise_role_name_exists_in_team(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
    mock_role: Mock,
) -> None:
    # given
    mock_role_repository.find.return_value = mock_role

    # when
    with (
        patch.object(TeamRoleService, "validate_not_modify_owner_role", return_value=None),
        patch.object(
            TeamRoleService,
            "validate_role_name_not_exists_in_team",
            side_effect=RoleNameExistsInTeamException("test"),
        ),
    ):
        with pytest.raises(RoleNameExistsInTeamException):
            await team_role_service.update_role(
                role_id=1,
                team_id=uuid4(),
                role_update_dto=RoleUpdateDto(
                    name="test diff", description="test", scopes={"test"}
                ),
            )


async def test_delete_role(
    team_role_service: TeamRoleService,
    mock_role_repository: AsyncMock,
) -> None:
    # when
    with patch.object(TeamRoleService, "validate_not_modify_owner_role", return_value=None):
        await team_role_service.delete_role(role_id=1, team_id=uuid4())

    # then
    mock_role_repository.delete_by_id_and_team_id.assert_called_once()


async def test_delete_role_raise_modify_owner_role(
    team_role_service: TeamRoleService,
) -> None:
    # when
    with patch.object(
        TeamRoleService,
        "validate_not_modify_owner_role",
        side_effect=CannotModifyOwnerRoleException,
    ):
        with pytest.raises(CannotModifyOwnerRoleException):
            await team_role_service.delete_role(role_id=1, team_id=uuid4())
