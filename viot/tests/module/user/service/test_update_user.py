from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.user.dto import UserUpdateDto
from app.module.user.exception import UserNotFoundException
from app.module.user.service import UserService


async def test_success(
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


async def test_fail__user_not_found(
    user_service: UserService, mock_user_repository: AsyncMock
) -> None:
    mock_user_repository.find.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.update_user(
            user_id=uuid4(),
            user_update_dto=UserUpdateDto(first_name="New Name", last_name="New Last Name"),
        )
