from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.module.auth.dto.auth_dto import LoginDto, RegisterDto
from app.module.auth.exception.auth_exception import (
    InvalidCredentialsException,
    InvalidVerifyEmailTokenException,
)
from app.module.auth.exception.user_exception import UserEmailAlreadyExistsException
from app.module.auth.service.auth_service import AuthService


async def test_login_correctly(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    login_dto = LoginDto(email=mock_user.email, password=mock_user.raw_password)
    mock_user_repository.find_by_email.return_value = mock_user

    # when
    result = await auth_service.login(login_dto=login_dto)

    # then
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.access_token_expires_at is not None


async def test_login_raises_when_invalid_password(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    login_dto = LoginDto(email=mock_user.email, password=mock_user.raw_password + "invalid")
    mock_user_repository.find_by_email.return_value = mock_user

    # when
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login(login_dto=login_dto)

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_user_repository.save.assert_not_called()


async def test_login_raises_when_user_not_found(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    login_dto = LoginDto(email=mock_user.email, password=mock_user.raw_password)
    mock_user_repository.find_by_email.return_value = None

    # when
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login(login_dto=login_dto)

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_user_repository.save.assert_not_called()


async def test_register_correctly(
    auth_service: AuthService,
    mock_email_service: Mock,
    mock_user_repository: AsyncMock,
    mock_user: Mock,
    mock_request_ctx: None,
) -> None:
    # given
    register_dto = RegisterDto(
        email=mock_user.email,
        password=mock_user.raw_password,
        first_name=mock_user.first_name,
        last_name=mock_user.last_name,
    )
    mock_user_repository.exists_by_email.return_value = False
    mock_user_repository.save.return_value = mock_user
    mock_email_service.send_verify_account_email.return_value = None

    # when
    result = await auth_service.register(register_dto=register_dto)

    # then
    assert result.id == mock_user.id
    assert result.first_name == mock_user.first_name
    assert result.last_name == mock_user.last_name
    assert result.email == mock_user.email
    assert result.role == mock_user.role
    assert result.created_at == mock_user.created_at
    assert result.updated_at is None

    mock_user_repository.exists_by_email.assert_called_once_with(email=mock_user.email)
    mock_user_repository.save.assert_called_once()
    mock_email_service.send_verify_account_email.assert_called_once()


async def test_register_raises_when_email_already_exists(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    register_dto = RegisterDto(
        email=mock_user.email,
        password=mock_user.raw_password,
        first_name=mock_user.first_name,
        last_name=mock_user.last_name,
    )
    mock_user_repository.exists_by_email.return_value = True

    # when
    with pytest.raises(UserEmailAlreadyExistsException):
        await auth_service.register(register_dto=register_dto)

    # then
    mock_user_repository.exists_by_email.assert_called_once_with(email=mock_user.email)


async def test_logout_correctly(
    auth_service: AuthService, mock_refresh_token_repository: AsyncMock, mock_user: Mock
) -> None:
    # given

    # when
    await auth_service.logout(refresh_token="refresh_token")

    # then
    mock_refresh_token_repository.update_token_expires_at.assert_called_once()


async def test_verify_account_correctly(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.update_email_verified_at.return_value = None

    # when
    with patch(
        "app.module.auth.service.auth_service.parse_jwt_token",
        lambda x: {"user_id": str(mock_user.id)},  # type: ignore
    ):
        await auth_service.verify_account(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_called_once()


async def test_verify_account_raises_when_invalid_token(
    auth_service: AuthService,
    mock_user_repository: AsyncMock,
) -> None:
    # given

    # when
    with patch("app.module.auth.service.auth_service.parse_jwt_token", side_effect=Exception()):
        with pytest.raises(InvalidVerifyEmailTokenException):
            await auth_service.verify_account(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_not_called()


async def test_verify_account_raises_when_user_not_found(
    auth_service: AuthService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.update_email_verified_at.side_effect = Exception()

    # when
    with patch(
        "app.module.auth.service.auth_service.parse_jwt_token",
        lambda x: {"user_id": str(mock_user.id)},  # type: ignore
    ):
        with pytest.raises(InvalidVerifyEmailTokenException):
            await auth_service.verify_account(token="token")

    # then
    mock_user_repository.update_email_verified_at.assert_called_once()
