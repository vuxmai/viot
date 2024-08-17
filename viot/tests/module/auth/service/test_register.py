from unittest.mock import AsyncMock, Mock

import pytest

from app.module.auth.dto import RegisterDto
from app.module.auth.service import AuthService
from app.module.user.exception import UserEmailAlreadyExistsException


async def test_correctly(
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


async def test_raises_when_email_already_exists(
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
