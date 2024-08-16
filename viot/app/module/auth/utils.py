import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.config import settings

from .constant import BCRYPT_SALT_ROUNDS
from .exception import InvalidTokenException, TokenExpiredException

logger = logging.getLogger(__name__)


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
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG), expire_at


def parse_jwt_token(token: str) -> dict[str, Any]:
    """Parse a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except Exception as e:
        logger.warning(f"Failed to parse JWT token: {e}")
        raise InvalidTokenException


def hash_password(password: str, salt_rounds: int = BCRYPT_SALT_ROUNDS) -> bytes:
    """Hash a password with bcrypt."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt(salt_rounds)
    return bcrypt.hashpw(pw, salt)


def verify_password(password: str, password_in_db: bytes) -> bool:
    """Verify a password against a hashed password in the database."""
    pw = bytes(password, "utf-8")
    return bcrypt.checkpw(pw, password_in_db)
