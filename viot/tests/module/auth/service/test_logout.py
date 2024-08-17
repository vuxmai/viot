from unittest.mock import AsyncMock, Mock

from app.module.auth.service import AuthService


async def test_correctly(
    auth_service: AuthService, mock_refresh_token_repository: AsyncMock, mock_user: Mock
) -> None:
    # given

    # when
    await auth_service.logout(user_id=mock_user.id, refresh_token="refresh_token")

    # then
    mock_refresh_token_repository.delete.assert_called_once_with(
        user_id=mock_user.id,
        token="refresh_token",
    )
