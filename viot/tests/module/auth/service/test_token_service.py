from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from faker import Faker

from app.module.auth.constants import REFRESH_TOKEN_DURATION_SEC, ViotUserRole
from app.module.auth.exception.auth_exception import InvalidCredentialsException
from app.module.auth.exception.token_exception import InvalidRefreshTokenException
from app.module.auth.model.refresh_token import RefreshToken
from app.module.auth.model.user import User
from app.module.auth.service.token_service import TokenService
from app.module.auth.utils.password_utils import hash_password


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_refresh_token_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def token_service(
    mock_user_repository: AsyncMock, mock_refresh_token_repository: AsyncMock
) -> TokenService:
    return TokenService(
        user_repository=mock_user_repository,
        refresh_token_repository=mock_refresh_token_repository,
    )


@pytest.fixture
def mock_user() -> Mock:
    user = Mock(spec=User)
    user.id = uuid4()
    user.first_name = Faker().first_name()
    user.last_name = Faker().last_name()
    user.email = Faker().email()
    user.email_verified_at = datetime.now()
    user.raw_password = "!abcABC123"
    user.password = hash_password("!abcABC123")
    user.role = ViotUserRole.USER
    user.disabled = False
    user.created_at = datetime.now(UTC)
    user.updated_at = None
    user.verified = True
    return user


@pytest.fixture
def mock_refresh_token(mock_user: Mock) -> Mock:
    refresh_token = Mock(spec=RefreshToken)
    refresh_token.id = uuid4()
    refresh_token.user_id = mock_user.id
    refresh_token.token = uuid4().hex
    refresh_token.expires_at = datetime.now(UTC) + timedelta(seconds=REFRESH_TOKEN_DURATION_SEC)
    return refresh_token


async def test_renew_token_correctly(
    token_service: TokenService,
    mock_refresh_token_repository: AsyncMock,
    mock_user_repository: AsyncMock,
    mock_user: Mock,
    mock_refresh_token: Mock,
) -> None:
    # given
    mock_refresh_token_repository.find_by_token.return_value = mock_refresh_token
    mock_user_repository.find.return_value = mock_user
    mock_refresh_token_repository.save.return_value = mock_refresh_token

    # when
    result = await token_service.renew_token(refresh_token=mock_refresh_token.token)

    # then
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.access_token_expires_at is not None


async def test_renew_token_raises_when_refresh_token_not_found(
    token_service: TokenService,
    mock_refresh_token_repository: AsyncMock,
) -> None:
    # given
    mock_refresh_token_repository.find_by_token.return_value = None

    # when
    with pytest.raises(InvalidCredentialsException):
        await token_service.renew_token(refresh_token="refresh_token")


async def test_renew_token_raises_when_refresh_token_is_expired(
    token_service: TokenService,
    mock_refresh_token_repository: AsyncMock,
    mock_refresh_token: Mock,
) -> None:
    # given
    mock_refresh_token_repository.find_by_token.return_value = mock_refresh_token
    mock_refresh_token.expires_at = datetime.now(UTC) - timedelta(days=1)

    # when
    with pytest.raises(InvalidRefreshTokenException):
        await token_service.renew_token(refresh_token=mock_refresh_token.token)
