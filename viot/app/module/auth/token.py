from datetime import timedelta
from typing import Any
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.config import settings

from .constant import JWT_ACCESS_TOKEN_EXP, JWT_REFRESH_TOKEN_EXP
from .dto import AccessToken, RefreshToken
from .utils import create_jwt_token, parse_jwt_token


def create_refresh_token(*, user_id: UUID, email: str) -> tuple[str, int]:
    refresh_token = RefreshToken(user_id=user_id, email=email)
    return create_jwt_token(
        payload=jsonable_encoder(refresh_token),
        expire_duration=timedelta(seconds=JWT_REFRESH_TOKEN_EXP),
    )


def create_access_token(*, user_id: UUID, email: str) -> tuple[str, int]:
    access_token = AccessToken(sub=user_id, email=email)
    return create_jwt_token(
        payload=jsonable_encoder(access_token),
        expire_duration=timedelta(seconds=JWT_ACCESS_TOKEN_EXP),
    )


def parse_access_token(token: str) -> AccessToken:
    return AccessToken.model_validate(parse_jwt_token(token))


def parse_refresh_token(token: str) -> RefreshToken:
    return RefreshToken.model_validate(parse_jwt_token(token))


def get_refresh_token_settings(refresh_token: str, expired: bool = False) -> dict[str, Any]:
    base_cookie = {
        "key": "refreshToken",
        "httponly": True,
        "samesite": settings.JWT_REFRESH_TOKEN_SAMESITE,
        "secure": settings.JWT_REFRESH_TOKEN_SECURE,
        "domain": settings.DOMAIN,
        "value": refresh_token if not expired else "",
        "max_age": JWT_REFRESH_TOKEN_EXP if not expired else 0,
    }
    return base_cookie
