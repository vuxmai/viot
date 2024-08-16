import re

# Password
BCRYPT_SALT_ROUNDS = 12
PASSWORD_REGEX_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,20}$")
PASSWORD_REGEX_VALIDATION_ERROR_MSG = (
    "Password must be between 8 and 20 characters and contain at least "
    "one digit, one uppercase letter, and one special character"
)

# JWT
JWT_ACCESS_TOKEN_EXP = 60 * 10  # 10 minutes
JWT_REFRESH_TOKEN_EXP = 60 * 60 * 24 * 7  # 7 days

# Redis prefixes
REDIS_REFRESH_TOKEN_PREFIX = "rf"
REDIS_RESET_PASSWORD_PREFIX = "rp"

# Email
VERIFY_EMAIL_TOKEN_EXP = 60 * 60 * 24  # 24 hours
FORGOT_PASSWORD_TOKEN_EXP = 60 * 60  # 1 hour
