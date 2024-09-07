import logging
import uuid
from datetime import UTC, datetime, timedelta
from uuid import UUID

from injector import inject

from app.config import app_settings
from app.module.email.service import IEmailService

from ..constants import EMAIL_VERIFICATION_DURATION_SEC, REFRESH_TOKEN_DURATION_SEC, ViotUserRole
from ..dto.auth_dto import (
    LoginDto,
    RegisterDto,
    TokenDto,
)
from ..dto.user_dto import UserDto
from ..exception.auth_exception import InvalidCredentialsException, InvalidVerifyEmailTokenException
from ..exception.user_exception import UserEmailAlreadyExistsException
from ..model.refresh_token import RefreshToken
from ..model.user import User
from ..repository.password_reset_repository import PasswordResetRepository
from ..repository.refresh_token_repository import RefreshTokenRepository
from ..repository.user_repository import UserRepository
from ..utils.jwt_utils import create_jwt_token, parse_jwt_token
from ..utils.password_utils import hash_password, verify_password
from ..utils.token_utils import AccessToken, create_access_token

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

        rf_token = (
            await self._refresh_token_repository.save(
                obj=RefreshToken(
                    user_id=user.id,
                    token=uuid.uuid4().hex,
                    expires_at=datetime.now().replace(tzinfo=None)
                    + timedelta(seconds=REFRESH_TOKEN_DURATION_SEC),
                )
            )
        ).token
        ac_token, ac_expire = create_access_token(access_token=AccessToken(user_id=user.id))

        return TokenDto(
            access_token=ac_token, refresh_token=rf_token, access_token_expires_at=ac_expire
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
                role=ViotUserRole.USER,
            )
        )

        verify_token, _ = create_jwt_token(
            payload={"user_id": str(user.id)},
            expire_duration=timedelta(seconds=EMAIL_VERIFICATION_DURATION_SEC),
        )

        self._email_service.send_verify_account_email(
            email=user.email,
            name=user.first_name,
            verify_url=f"{app_settings.API_SERVER_URL}{app_settings.API_PREFIX}/auth/verify-email?token={verify_token}",
        )

        return UserDto.from_model(user)

    async def logout(self, *, refresh_token: str) -> None:
        try:
            await self._refresh_token_repository.update_token_expires_at(
                token=refresh_token, expires_at=datetime.now(UTC)
            )
        except Exception as e:
            logger.warning(f"Failed to logout: {e}")
            raise InvalidCredentialsException

    async def verify_account(self, *, token: str) -> None:
        try:
            payload = parse_jwt_token(token)
            user_id = UUID(payload.get("user_id"))
            await self._user_repository.update_email_verified_at(
                user_id=user_id, email_verified_at=datetime.now().replace(tzinfo=None)
            )
        except Exception as e:
            logger.warning(f"Failed to verify email: {e}")
            raise InvalidVerifyEmailTokenException
