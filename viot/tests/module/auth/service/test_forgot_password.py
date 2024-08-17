from unittest.mock import AsyncMock, Mock

from app.module.auth.service import AuthService


async def test_correctly(
    auth_service: AuthService,
    mock_email_service: Mock,
    mock_user_repository: AsyncMock,
    mock_user: Mock,
    mock_request_ctx: None,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = mock_user
    mock_email_service.send_reset_password_email.return_value = None

    # when
    await auth_service.forgot_password(email=mock_user.email)

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email=mock_user.email)
    mock_email_service.send_reset_password_email.assert_called_once()


async def test_correctly_when_user_not_found(
    auth_service: AuthService,
    mock_user_repository: AsyncMock,
    mock_email_service: Mock,
    mock_request_ctx: None,
) -> None:
    # given
    mock_user_repository.find_by_email.return_value = None

    # when
    await auth_service.forgot_password(email="user@example.com")

    # then
    mock_user_repository.find_by_email.assert_called_once_with(email="user@example.com")
    mock_email_service.send_reset_password_email.assert_not_called()
