from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.auth.dto.user_dto import ChangePasswordDto, UserUpdateDto
from app.module.auth.exception.user_exception import (
    PasswordNotMatchException,
    UserNotFoundException,
)
from app.module.auth.service.user_service import UserService


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def user_service(mock_user_repository: AsyncMock) -> UserService:
    return UserService(user_repository=mock_user_repository)


async def test_change_password_correctly(
    user_service: UserService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    new_password = "!defDEF456"
    mock_user_repository.find.return_value = mock_user
    mock_user_repository.update_password.return_value = mock_user

    await user_service.change_password(
        user_id=mock_user.id,
        change_password_dto=ChangePasswordDto(
            old_password=mock_user.raw_password, new_password=new_password
        ),
    )

    mock_user_repository.update_password.assert_awaited_once()


async def test_change_password_raises_when_user_not_found(
    user_service: UserService, mock_user_repository: AsyncMock
) -> None:
    mock_user_repository.find.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.change_password(
            user_id=uuid4(),
            change_password_dto=ChangePasswordDto(
                old_password="!abcABC123", new_password="!defDEF456"
            ),
        )


async def test_change_password_raises_when_password_not_match(
    user_service: UserService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    mock_user_repository.find.return_value = mock_user

    with pytest.raises(PasswordNotMatchException):
        await user_service.change_password(
            user_id=mock_user.id,
            change_password_dto=ChangePasswordDto(
                old_password=mock_user.raw_password + "invalid", new_password="!defDEF456"
            ),
        )


async def test_update_user_correctly(
    user_service: UserService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    mock_user_repository.find.return_value = mock_user
    dto = UserUpdateDto(first_name="New Name", last_name="New Last Name")
    # Update mock_user with new values
    mock_user.first_name = dto.first_name
    mock_user.last_name = dto.last_name
    mock_user_repository.save.return_value = mock_user

    await user_service.update_user(user_id=mock_user.id, user_update_dto=dto)

    mock_user_repository.save.assert_called_once_with(mock_user)


async def test_update_user_raises_when_user_not_found(
    user_service: UserService, mock_user_repository: AsyncMock
) -> None:
    mock_user_repository.find.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.update_user(
            user_id=uuid4(),
            user_update_dto=UserUpdateDto(first_name="New Name", last_name="New Last Name"),
        )


async def test_delete_user_correctly(
    user_service: UserService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # when
    await user_service.delete_user_by_id(user_id=mock_user.id)

    # then
    mock_user_repository.delete_by_id.assert_called_once_with(mock_user.id)
