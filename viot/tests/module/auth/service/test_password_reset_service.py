from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from faker import Faker

from app.common.fastapi.context import request_ctx
from app.module.auth.constants import FORGOT_PASSWORD_DURATION_SEC, ViotUserRole
from app.module.auth.dto.reset_password_dto import ResetPasswordDto
from app.module.auth.exception.auth_exception import (
    InvalidResetPasswordTokenException,
    ResetPasswordTokenExpiredException,
)
from app.module.auth.model.password_reset import PasswordReset
from app.module.auth.model.user import User
from app.module.auth.service.password_reset_service import PasswordResetService
from app.module.auth.utils.password_utils import hash_password


@pytest.fixture(scope="function", autouse=True)
def mock_request_ctx() -> Generator[None, None, None]:
    token = request_ctx.set(Mock())
    yield
    request_ctx.reset(token)


@pytest.fixture
def mock_email_service() -> Mock:
    return Mock()


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_password_reset_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def password_reset_service(
    mock_email_service: Mock,
    mock_user_repository: AsyncMock,
    mock_password_reset_repository: AsyncMock,
) -> PasswordResetService:
    return PasswordResetService(
        email_service=mock_email_service,
        user_repository=mock_user_repository,
        password_reset_repository=mock_password_reset_repository,
    )


@pytest.fixture
def mock_user() -> Mock:
    user = Mock(spec=User)
    user.id = uuid4()
    user.first_name = Faker().first_name()
    user.last_name = Faker().last_name()
    user.email = Faker().email()
    user.email_verified_at = datetime.now()
    user.raw_password = "!abcABC123"
    user.password = hash_password("!abcABC123")
    user.role = ViotUserRole.USER
    user.disabled = False
    user.created_at = datetime.now(UTC)
    user.updated_at = None
    user.verified = True
    return user


@pytest.fixture
def mock_password_reset(mock_user: Mock) -> Mock:
    password_reset = Mock(spec=PasswordReset)
    password_reset.email = mock_user.email
    password_reset.token = uuid4().hex
    password_reset.created_at = datetime.now(UTC)
    return password_reset


async def test_forgot_password_correctly(
    password_reset_service: PasswordResetService,
    mock_email_service: Mock,
    mock_user_repository: AsyncMock,
    mock_user: Mock,
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
    dto = ResetPasswordDto(
        token=mock_password_reset.token, password=mock_user.raw_password + "diff"
    )
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
