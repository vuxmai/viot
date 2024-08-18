from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.user.dto import ChangePasswordDto
from app.module.user.exception import PasswordNotMatchException, UserNotFoundException
from app.module.user.service import UserService


async def test_correctly(
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


async def test_raises_when_user_not_found(
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


async def test_raises_when_password_not_match(
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
