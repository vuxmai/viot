import uuid
from datetime import datetime, timedelta

from injector import inject

from app.config import app_settings
from app.module.email.service import IEmailService

from ..constants import FORGOT_PASSWORD_DURATION_SEC
from ..dto.reset_password_dto import ResetPasswordDto
from ..exception.auth_exception import (
    InvalidResetPasswordTokenException,
    ResetPasswordTokenExpiredException,
)
from ..model.password_reset import PasswordReset
from ..repository.password_reset_repository import PasswordResetRepository
from ..repository.user_repository import UserRepository
from ..utils.password_utils import hash_password


class PasswordResetService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        password_reset_repository: PasswordResetRepository,
        email_service: IEmailService,
    ):
        self._user_repository = user_repository
        self._password_reset_repository = password_reset_repository
        self._email_service = email_service

    async def forgot_password(self, *, email: str) -> None:
        user = await self._user_repository.find_by_email(email=email)
        if not user:
            return

        password_reset = PasswordReset(email=user.email, token=uuid.uuid4().hex)
        password_reset = await self._password_reset_repository.save(password_reset)

        reset_url = f"{app_settings.UI_URL}/auth/reset-password?token={password_reset.token}"
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
        if (
            password_reset.created_at + timedelta(seconds=FORGOT_PASSWORD_DURATION_SEC)
            < datetime.now()
        ):
            raise ResetPasswordTokenExpiredException

        user = await self._user_repository.find_by_email(email=password_reset.email)
        if not user:
            raise InvalidResetPasswordTokenException

        await self._user_repository.update_password(
            user_id=user.id, hashed_password=hash_password(reset_password_dto.password)
        )

        await self._password_reset_repository.delete(password_reset)
