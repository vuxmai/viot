import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from injector import inject

from app.common.fastapi.context import request_ctx
from app.config import settings
from app.module.email.service import IEmailService
from app.module.user.dto import UserDto
from app.module.user.exception import UserEmailAlreadyExistsException
from app.module.user.model import User
from app.module.user.repository import UserRepository

from .constant import FORGOT_PASSWORD_TOKEN_EXP, VERIFY_EMAIL_TOKEN_EXP
from .dto import (
    LoginDto,
    RegisterDto,
    ResetPasswordDto,
    TokenDto,
)
from .exception import (
    InvalidCredentialsException,
    InvalidResetPasswordTokenException,
    InvalidVerifyEmailTokenException,
    ResetPasswordTokenExpiredException,
)
from .model import PasswordReset
from .repository import PasswordResetRepository, RefreshTokenRepository
from .token import (
    create_access_token,
    create_refresh_token,
    parse_refresh_token,
)
from .utils import create_jwt_token, hash_password, parse_jwt_token, verify_password

logger = logging.getLogger(__name__)


class AuthService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_reset_repository: PasswordResetRepository,
        email_service: IEmailService,
    ) -> None:
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._password_reset_repository = password_reset_repository
        self._email_service = email_service

    async def login(self, *, login_dto: LoginDto) -> TokenDto:
        user = await self._user_repository.find_by_email(email=login_dto.email)
        if not user or not verify_password(login_dto.password, user.password):
            raise InvalidCredentialsException

        rf_token, rf_expire = create_refresh_token(user_id=user.id, email=user.email)
        ac_token, ac_expire = create_access_token(user_id=user.id, email=user.email)

        await self._refresh_token_repository.save(user_id=user.id, token=rf_token)

        # Pydantic datetime can handle timestamp
        return TokenDto(
            access_token=ac_token,
            refresh_token=rf_token,
            access_token_expires_at=ac_expire,  # type: ignore
            refresh_token_expires_at=rf_expire,  # type: ignore
        )

    async def register(self, *, register_dto: RegisterDto) -> UserDto:
        if await self._user_repository.exists_by_email(email=register_dto.email):
            raise UserEmailAlreadyExistsException

        user = await self._user_repository.save(
            User(
                email=register_dto.email,
                password=hash_password(register_dto.password),
                first_name=register_dto.first_name,
                last_name=register_dto.last_name,
            )
        )

        verify_token = create_jwt_token(
            payload={"user_id": str(user.id)},
            expire_duration=timedelta(seconds=VERIFY_EMAIL_TOKEN_EXP),
        )

        base_url = str(request_ctx.value.base_url).strip("/")
        self._email_service.send_verify_account_email(
            email=user.email,
            name=user.first_name,
            verify_url=f"{base_url}{settings.API_PREFIX}/auth/verify-email?token={verify_token}",
        )

        return UserDto.from_model(user)

    async def logout(self, *, user_id: UUID, refresh_token: str) -> None:
        await self._refresh_token_repository.delete(user_id=user_id, token=refresh_token)
        # May be we should implement a blacklist for the access token

    async def renew_token(self, *, refresh_token: str) -> TokenDto:
        result = parse_refresh_token(refresh_token)

        if not await self._refresh_token_repository.exists(
            user_id=result.user_id, token=refresh_token
        ):
            raise InvalidCredentialsException

        rf_token, rf_expire = create_refresh_token(user_id=result.user_id, email=result.email)
        ac_token, ac_expire = create_access_token(user_id=result.user_id, email=result.email)

        await self._refresh_token_repository.delete(user_id=result.user_id, token=refresh_token)
        await self._refresh_token_repository.save(user_id=result.user_id, token=rf_token)

        return TokenDto(
            access_token=ac_token,
            refresh_token=rf_token,
            access_token_expires_at=ac_expire,  # type: ignore
            refresh_token_expires_at=rf_expire,  # type: ignore
        )

    async def forgot_password(self, *, email: str) -> None:
        user = await self._user_repository.find_by_email(email=email)
        if not user:
            return

        password_reset = PasswordReset(email=user.email)
        password_reset = await self._password_reset_repository.save(password_reset)

        reset_url = f"{settings.UI_URL}/auth/reset-password?token={password_reset.token}"
        self._email_service.send_reset_password_email(
            email=user.email, name=user.first_name, link=reset_url
        )

    async def reset_password(self, *, reset_password_dto: ResetPasswordDto) -> None:
        password_reset = await self._password_reset_repository.find_by_token(
            token=reset_password_dto.token
        )
        if not password_reset:
            raise InvalidResetPasswordTokenException

        # Check if token is expired
        if password_reset.created_at + timedelta(seconds=FORGOT_PASSWORD_TOKEN_EXP) < datetime.now(
            UTC
        ):
            raise ResetPasswordTokenExpiredException

        user = await self._user_repository.find_by_email(email=password_reset.email)
        if not user:
            raise InvalidResetPasswordTokenException

        await self._user_repository.update_password(
            user_id=user.id, hashed_password=hash_password(reset_password_dto.password)
        )

        await self._password_reset_repository.delete(password_reset)

    async def verify_email(self, *, token: str) -> None:
        try:
            payload = parse_jwt_token(token)
            user_id = UUID(payload.get("user_id"))
            await self._user_repository.update_email_verified_at(
                user_id=user_id, email_verified_at=datetime.now().replace(tzinfo=None)
            )
        except Exception as e:
            logger.warning(f"Failed to verify email: {e}")
            raise InvalidVerifyEmailTokenException
