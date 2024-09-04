import uuid
from datetime import datetime, timedelta
from typing import Any

import jwt

from ..config import auth_settings
from ..constants import JWT_ALG
from ..exception.token_exception import InvalidTokenException, TokenExpiredException


def create_jwt_token(
    *, payload: dict[str, Any] | None = None, expire_duration: timedelta
) -> tuple[str, int]:
    """Create a JWT token with the given payload and expiration time."""
    if payload is None:
        payload = {}
    issue_at = int(datetime.now().timestamp())
    expire_at = issue_at + int(expire_duration.total_seconds())
    payload["exp"] = expire_at
    payload["iat"] = issue_at
    payload["jti"] = str(uuid.uuid4())
    return jwt.encode(payload, auth_settings.JWT_SECRET, algorithm=JWT_ALG), expire_at


def parse_jwt_token(token: str) -> dict[str, Any]:
    """Parse a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[JWT_ALG])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except Exception:
        raise InvalidTokenException
