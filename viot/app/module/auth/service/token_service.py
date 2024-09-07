import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

from injector import inject

from app.config import app_settings

from ..constants import REFRESH_TOKEN_DURATION_SEC, REFRESH_TOKEN_SAMESITE, REFRESH_TOKEN_SECURE
from ..dto.auth_dto import TokenDto
from ..exception.auth_exception import InvalidCredentialsException
from ..exception.token_exception import InvalidRefreshTokenException, TokenExpiredException
from ..model.refresh_token import RefreshToken
from ..repository.refresh_token_repository import RefreshTokenRepository
from ..repository.user_repository import UserRepository
from ..utils.token_utils import AccessToken, create_access_token

logger = logging.getLogger(__name__)


class TokenService:
    @inject
    def __init__(
        self, user_repository: UserRepository, refresh_token_repository: RefreshTokenRepository
    ) -> None:
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository

    async def renew_token(self, *, refresh_token: str) -> TokenDto:
        rf_token_model = await self._refresh_token_repository.find_by_token(refresh_token)
        if not rf_token_model:
            raise InvalidCredentialsException

        # Check if token is expired
        if rf_token_model.expires_at < datetime.now():
            raise TokenExpiredException

        user = await self._user_repository.find(rf_token_model.user_id)
        if not user:
            raise InvalidCredentialsException

        # Check if the provided refresh token is the latest one
        latest_token = await self._refresh_token_repository.find_latest_token_by_user_id(user.id)
        if latest_token != refresh_token:
            # The provided refresh token is not the latest one
            # Invalidate all tokens and force user to login again
            await self._refresh_token_repository.update_all_tokens_expires_at(
                user_id=user.id, expires_at=datetime.now()
            )
            logger.warning("Provided refresh token is not the latest one. Invalidate all tokens.")
            raise InvalidRefreshTokenException

        refresh_token = (
            await self._refresh_token_repository.save(
                RefreshToken(
                    user_id=user.id,
                    token=uuid.uuid4().hex,
                    expires_at=datetime.now() + timedelta(seconds=REFRESH_TOKEN_DURATION_SEC),
                )
            )
        ).token
        ac_token, ac_expire_at = create_access_token(access_token=AccessToken(user_id=user.id))

        return TokenDto(
            access_token=ac_token,
            refresh_token=refresh_token,
            access_token_expires_at=ac_expire_at,
        )

    def get_refresh_token_settings(
        self, refresh_token: str, expired: bool = False
    ) -> dict[str, Any]:
        return {
            "key": "refreshToken",
            "httponly": True,
            "samesite": REFRESH_TOKEN_SAMESITE,
            "secure": REFRESH_TOKEN_SECURE,
            "domain": f".{app_settings.DOMAIN}",
            "value": refresh_token if not expired else "",
            "max_age": REFRESH_TOKEN_DURATION_SEC if not expired else 0,
        }
