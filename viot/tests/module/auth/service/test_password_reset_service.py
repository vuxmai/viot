from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from app.module.auth.constants import FORGOT_PASSWORD_DURATION_SEC
from app.module.auth.dto.reset_password_dto import ResetPasswordDto
from app.module.auth.exception.auth_exception import (
    InvalidResetPasswordTokenException,
    ResetPasswordTokenExpiredException,
)
from app.module.auth.service.password_reset_service import PasswordResetService


async def test_forgot_password_correctly(
    password_reset_service: PasswordResetService,
    mock_email_service: Mock,
    mock_user_repository: AsyncMock,
    mock_user: Mock,
    mock_request_ctx: None,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = mock_user
    mock_email_service.send_reset_password_email.return_value = None

    # when
    await password_reset_service.forgot_password(email=mock_user.email)

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_email_service.send_reset_password_email.assert_called_once()


async def test_forgot_password_correctly_when_user_not_found(
    password_reset_service: PasswordResetService,
    mock_user_repository: AsyncMock,
    mock_email_service: Mock,
    mock_request_ctx: None,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = None

    # when
    await password_reset_service.forgot_password(email="user@example.com")

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email="user@example.com")
    mock_email_service.send_reset_password_email.assert_not_called()


async def test_reset_password_correctly(
    password_reset_service: PasswordResetService,
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
    await password_reset_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_user_repository.update_password.assert_called_once()
    mock_password_reset_repository.delete.assert_called_once_with(mock_password_reset)


async def test_reset_password_raises_when_token_not_found(
    password_reset_service: PasswordResetService,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = None

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    with pytest.raises(InvalidResetPasswordTokenException):
        await password_reset_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )


async def test_reset_password_raises_when_token_expired(
    password_reset_service: PasswordResetService,
    mock_password_reset_repository: AsyncMock,
    mock_user: Mock,
    mock_password_reset: Mock,
) -> None:
    # given
    mock_password_reset_repository.find_by_token.return_value = mock_password_reset
    mock_password_reset.created_at = datetime.now(UTC) - timedelta(
        seconds=FORGOT_PASSWORD_DURATION_SEC
    )

    # when
    dto = ResetPasswordDto(token=mock_password_reset.token, password=mock_user.raw_password)
    with pytest.raises(ResetPasswordTokenExpiredException):
        await password_reset_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )


async def test_reset_password_raises_when_user_not_found(
    password_reset_service: PasswordResetService,
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
        await password_reset_service.reset_password(reset_password_dto=dto)

    # then
    mock_password_reset_repository.find_by_token.assert_called_once_with(
        token=mock_password_reset.token
    )
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
