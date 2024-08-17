from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.module.auth.exception import InvalidCredentialsException
from app.module.auth.service import AuthService


@patch("app.module.auth.service.parse_refresh_token")
async def test_correctly(
    mock_parse_refresh_token: Mock,
    auth_service: AuthService,
    mock_refresh_token_repository: AsyncMock,
    mock_user: Mock,
) -> None:
    # given
    mock_parse_refresh_token.return_value = Mock(
        user_id=mock_user.id,
        email=mock_user.email,
    )
    mock_refresh_token_repository.exists.return_value = True
    mock_refresh_token_repository.save.return_value = None
    mock_refresh_token_repository.delete.return_value = None

    # when
    result = await auth_service.renew_token(refresh_token="refresh_token")

    # then
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.access_token_expires_at is not None
    assert result.refresh_token_expires_at is not None

    mock_parse_refresh_token.assert_called_once_with("refresh_token")
    mock_refresh_token_repository.exists.assert_called_once_with(
        user_id=mock_user.id,
        token="refresh_token",
    )
    mock_refresh_token_repository.delete.assert_called_once_with(
        user_id=mock_user.id,
        token="refresh_token",
    )
    mock_refresh_token_repository.save.assert_called_once()


@patch("app.module.auth.service.parse_refresh_token")
async def test_raises_when_refresh_token_not_found(
    mock_parse_refresh_token: Mock,
    auth_service: AuthService,
    mock_refresh_token_repository: AsyncMock,
    mock_user: Mock,
) -> None:
    # given
    mock_parse_refresh_token.return_value = Mock(
        user_id=mock_user.id,
        email=mock_user.email,
    )
    mock_refresh_token_repository.exists.return_value = False

    # when
    with pytest.raises(InvalidCredentialsException):
        await auth_service.renew_token(refresh_token="refresh_token")

    # then
    mock_parse_refresh_token.assert_called_once_with("refresh_token")
    mock_refresh_token_repository.exists.assert_called_once_with(
        user_id=mock_user.id,
        token="refresh_token",
    )
