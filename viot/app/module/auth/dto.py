from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.common.dto import BaseInDto, BaseOutDto, NameStr

from .constant import PASSWORD_REGEX_PATTERN, PASSWORD_REGEX_VALIDATION_ERROR_MSG


# Access token and refresh token diff in user_id key
class AccessToken(BaseOutDto):
    sub: UUID
    email: str


class RefreshToken(BaseOutDto):
    user_id: UUID
    email: str


class LoginDto(BaseInDto):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not PASSWORD_REGEX_PATTERN.match(password):
            raise ValueError(PASSWORD_REGEX_VALIDATION_ERROR_MSG)
        return password


class TokenDto(BaseOutDto):
    access_token: str
    refresh_token: str
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime


class RegisterDto(LoginDto):
    first_name: NameStr
    last_name: NameStr


class ForgotPasswordDto(BaseInDto):
    email: EmailStr


class ResetPasswordDto(BaseInDto):
    token: str
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not PASSWORD_REGEX_PATTERN.match(password):
            raise ValueError(PASSWORD_REGEX_VALIDATION_ERROR_MSG)
        return password