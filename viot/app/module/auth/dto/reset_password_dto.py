from pydantic import EmailStr, Field, field_validator

from app.common.dto import BaseInDto

from ..constants import PASSWORD_REGEX_PATTERN, PASSWORD_REGEX_VALIDATION_ERROR_MSG


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
