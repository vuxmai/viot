from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field, StringConstraints

from app.common.dto import BaseInDto, BaseOutDto

from ..model.team import Team

TeamName = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9][\w\s-]{2,30}[a-zA-Z0-9]$",
        strip_whitespace=True,
        min_length=4,
        max_length=32,
    ),
]

TeamSlug = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        strip_whitespace=True,
        min_length=3,
        max_length=48,
    ),
]


class TeamCreateDto(BaseInDto):
    name: TeamName
    description: str | None = Field(default=None, min_length=1, max_length=255)


class TeamUpdateDto(BaseInDto):
    name: TeamName | None = Field(default=None)
    slug: TeamSlug | None = Field(default=None)
    description: str | None = Field(default=None, min_length=1, max_length=255)


class TeamDto(BaseOutDto):
    id: UUID
    name: str
    slug: str
    description: str | None
    default: bool
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, team: Team) -> "TeamDto":
        return cls.model_validate(team)


class TeamWithRoleDto(BaseOutDto):
    id: UUID
    name: str
    slug: str
    description: str | None
    role: str

    @classmethod
    def from_model(cls, team: Team, role: str) -> "TeamWithRoleDto":
        return cls(
            id=team.id, name=team.name, slug=team.slug, description=team.description, role=role
        )
