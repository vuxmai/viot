from unittest.mock import AsyncMock

import pytest

from app.module.auth.repository import PasswordResetRepository, RefreshTokenRepository
from app.module.team.repository import TeamRepository, UserTeamRepository
from app.module.team_invitation.repository import TeamInvitationRepository
from app.module.user.repository import UserRepository


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
def mock_user_team_repository() -> AsyncMock:
    return AsyncMock(spec=UserTeamRepository)


@pytest.fixture
def mock_team_invitation_repository() -> AsyncMock:
    return AsyncMock(spec=TeamInvitationRepository)
