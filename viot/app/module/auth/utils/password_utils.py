import bcrypt

from app.module.auth.constants import BCRYPT_SALT_ROUNDS


def hash_password(password: str, salt_rounds: int = BCRYPT_SALT_ROUNDS) -> bytes:
    """Hash a password with bcrypt."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt(salt_rounds)
    return bcrypt.hashpw(pw, salt)


def verify_password(password: str, password_in_db: bytes) -> bool:
    """Verify a password against a hashed password in the database."""
    pw = bytes(password, "utf-8")
    return bcrypt.checkpw(pw, password_in_db)
