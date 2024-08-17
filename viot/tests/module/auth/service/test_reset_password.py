from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from app.module.auth.constant import FORGOT_PASSWORD_TOKEN_EXP
from app.module.auth.dto import ResetPasswordDto
from app.module.auth.exception import (
    InvalidResetPasswordTokenException,
    ResetPasswordTokenExpiredException,
)
from app.module.auth.service import AuthService


async def test_correctly(
    auth_service: AuthService,
    mock_user_repository: AsyncMock,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = mock_password_reset
    mock_user_repository.find_by_email.return_value = mock_user
    mock_user_repository.update_password.return_value = None
    mock_password_reset_repository.delete.return_value = None

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    await auth_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_user_repository.update_password.assert_called_once()
    mock_password_reset_repository.delete.assert_called_once_with(mock_password_reset)


async def test_raises_when_token_not_found(
    auth_service: AuthService,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = None

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    with pytest.raises(InvalidResetPasswordTokenException):
        await auth_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )


async def test_raises_when_token_expired(
    auth_service: AuthService,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = mock_password_reset
    mock_password_reset.created_at = datetime.now(UTC) - timedelta(
        seconds=FORGOT_PASSWORD_TOKEN_EXP
    )

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    with pytest.raises(ResetPasswordTokenExpiredException):
        await auth_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )


async def test_raises_when_user_not_found(
    auth_service: AuthService,
    mock_user_repository: AsyncMock,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = mock_password_reset
    mock_user_repository.find_by_email.return_value = None

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    with pytest.raises(InvalidResetPasswordTokenException):
        await auth_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
