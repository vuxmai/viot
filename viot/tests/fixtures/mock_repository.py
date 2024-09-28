from unittest.mock import AsyncMock

import pytest

from app.module.auth.repository.password_reset_repository import PasswordResetRepository
from app.module.auth.repository.permission_repository import PermissionRepository
from app.module.auth.repository.refresh_token_repository import RefreshTokenRepository
from app.module.auth.repository.role_permission_repository import RolePermissionRepository
from app.module.auth.repository.role_repository import RoleRepository
from app.module.auth.repository.user_repository import UserRepository
from app.module.auth.repository.user_team_role_repository import UserTeamRoleRepository
from app.module.team.repository.team_invitation_repository import (
    TeamInvitationRepository,
)
from app.module.team.repository.team_repository import TeamRepository


@pytest.fixture
def mock_refresh_token_repository() -> AsyncMock:
    return AsyncMock(spec=RefreshTokenRepository)


@pytest.fixture
def mock_password_reset_repository() -> AsyncMock:
    return AsyncMock(spec=PasswordResetRepository)


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def mock_team_repository() -> AsyncMock:
    return AsyncMock(spec=TeamRepository)


@pytest.fixture
def mock_permission_repository() -> AsyncMock:
    return AsyncMock(spec=PermissionRepository)


@pytest.fixture
def mock_role_repository() -> AsyncMock:
    return AsyncMock(spec=RoleRepository)


@pytest.fixture
def mock_role_permission_repository() -> AsyncMock:
    return AsyncMock(spec=RolePermissionRepository)


@pytest.fixture
def mock_user_team_role_repository() -> AsyncMock:
    return AsyncMock(spec=UserTeamRoleRepository)


@pytest.fixture
def mock_team_invitation_repository() -> AsyncMock:
    return AsyncMock(spec=TeamInvitationRepository)
