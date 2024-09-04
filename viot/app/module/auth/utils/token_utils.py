from datetime import timedelta
from uuid import UUID

import msgspec

from ..constants import ACCESS_TOKEN_DURATION_SEC
from ..exception.token_exception import InvalidTokenException
from .jwt_utils import create_jwt_token, parse_jwt_token


class AccessToken(msgspec.Struct):
    user_id: UUID


def create_access_token(access_token: AccessToken) -> tuple[str, int]:
    return create_jwt_token(
        payload={"sub": str(access_token.user_id)},
        expire_duration=timedelta(seconds=ACCESS_TOKEN_DURATION_SEC),
    )


def parse_access_token(token: str) -> AccessToken:
    payload = parse_jwt_token(token)
    try:
        return AccessToken(user_id=payload["sub"])
    except Exception:
        raise InvalidTokenException
