from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from app.module.auth.exception.auth_exception import InvalidCredentialsException
from app.module.auth.exception.token_exception import InvalidRefreshTokenException
from app.module.auth.service.token_service import TokenService


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
