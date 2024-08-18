from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.user.exception import UserNotFoundException
from app.module.user.service import UserService


async def test_success(
    user_service: UserService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    mock_user_repository.find.return_value = mock_user
    mock_user_repository.delete.return_value = None

    await user_service.delete_user(user_id=mock_user.id)

    mock_user_repository.delete.assert_called_once_with(mock_user)


async def test_fail__user_not_found(user_service: UserService, mock_user_repository: Mock) -> None:
    mock_user_repository.find.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.delete_user(user_id=uuid4())
