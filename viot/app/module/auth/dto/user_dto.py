from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.common.dto import BaseInDto, BaseOutDto, NameStr, PagingDto
from app.module.team.dto.team_dto import TeamWithRoleDto

from ..constants import PASSWORD_REGEX_PATTERN, PASSWORD_REGEX_VALIDATION_ERROR_MSG
from ..model.user import User


class ChangePasswordDto(BaseInDto):
    old_password: str = Field(..., min_length=8, max_length=20)
    new_password: str = Field(..., min_length=8, max_length=20)

    @model_validator(mode="after")
    def validate_passwords(self) -> Self:
        if self.old_password == self.new_password:
            raise ValueError("Old password and new password must be different")
        return self

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not PASSWORD_REGEX_PATTERN.match(password):
            raise ValueError(PASSWORD_REGEX_VALIDATION_ERROR_MSG)
        return password


class UserUpdateDto(BaseInDto):
    first_name: NameStr | None = Field(None)
    last_name: NameStr | None = Field(None)


class UserDto(BaseOutDto):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, user: User) -> "UserDto":
        return cls.model_validate(user)


class UserWithTeamsDto(UserDto):
    teams: list[TeamWithRoleDto]


class UserPagingDto(PagingDto[UserDto]):
    pass
