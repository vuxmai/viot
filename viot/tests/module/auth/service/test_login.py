from unittest.mock import AsyncMock, Mock

import pytest

from app.module.auth.dto import LoginDto
from app.module.auth.exception import InvalidCredentialsException
from app.module.auth.service import AuthService


async def test_correctly(
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
    assert result.refresh_token_expires_at is not None


async def test_raises_when_invalid_password(
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


async def test_raises_when_user_not_found(
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
