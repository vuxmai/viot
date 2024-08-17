from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.module.auth.exception import InvalidVerifyEmailTokenException
from app.module.auth.service import AuthService


async def test_correctly(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.update_email_verified_at.return_value = None

    # when
    with patch("app.module.auth.service.parse_jwt_token", lambda x: {"user_id": str(mock_user.id)}):  # type: ignore
        await auth_service.verify_email(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_called_once()


async def test_raises_when_invalid_token(
    auth_service: AuthService,
    mock_user_repository: AsyncMock,
) -> None:
    # given

    # when
    with patch("app.module.auth.service.parse_jwt_token", side_effect=Exception()):
        with pytest.raises(InvalidVerifyEmailTokenException):
            await auth_service.verify_email(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_not_called()


async def test_raises_when_user_not_found(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.update_email_verified_at.side_effect = Exception()

    # when
    with patch("app.module.auth.service.parse_jwt_token", lambda x: {"user_id": str(mock_user.id)}):  # type: ignore
        with pytest.raises(InvalidVerifyEmailTokenException):
            await auth_service.verify_email(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_called_once()
