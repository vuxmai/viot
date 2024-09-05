import re
from enum import StrEnum


class ViotUserRole(StrEnum):
    ADMIN = "Admin"
    USER = "User"


# Password constants
BCRYPT_SALT_ROUNDS = 12
PASSWORD_REGEX_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,20}$")
PASSWORD_REGEX_VALIDATION_ERROR_MSG = (
    "Password must be between 8 and 20 characters and contain at least "
    "one digit, one uppercase letter, and one special character"
)


# JWT constants
JWT_ALG = "HS256"
ACCESS_TOKEN_DURATION_SEC = 60 * 5  # 5 minutes
REFRESH_TOKEN_DURATION_SEC = 60 * 60 * 24 * 21  # 21 days
REFRESH_TOKEN_SAMESITE = "Lax"
REFRESH_TOKEN_SECURE = True


# Email verification token constants
EMAIL_VERIFICATION_DURATION_SEC = 60 * 60 * 24  # 24 hours
FORGOT_PASSWORD_DURATION_SEC = 60 * 60  # 1 hour