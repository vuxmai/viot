from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, field_validator

from app.common.dto import BaseInDto, BaseOutDto, PagingDto
from app.database.repository import Page
from app.module.team.constants import TeamRole

from ..model.team_invitation import TeamInvitation


class TeamInvitationCreateDto(BaseInDto):
    email: EmailStr
    role: TeamRole

    @field_validator("role", mode="before")
    def validate_role(cls, v: TeamRole) -> TeamRole:
        if v == TeamRole.OWNER:
            raise ValueError(f"{TeamRole.OWNER} role cannot be used for invitations")
        return v


class TeamInvitationAcceptDto(BaseInDto):
    token: str


class TeamInvitationDeclineDto(BaseInDto):
    token: str


class TeamInvitationRevokeDto(BaseInDto):
    token: str


class TeamInvitationDto(BaseOutDto):
    id: UUID
    email: str
    role: str
    created_at: datetime

    @classmethod
    def from_model(cls, invitation: TeamInvitation) -> "TeamInvitationDto":
        return cls(
            id=invitation.id,
            email=invitation.email,
            role=invitation.role,
            created_at=invitation.created_at,
        )


class PagingTeamInvitationDto(PagingDto[TeamInvitationDto]):
    @classmethod
    def from_page(cls, page: Page[TeamInvitation]) -> "PagingTeamInvitationDto":
        return cls(
            items=[TeamInvitationDto.from_model(invitation) for invitation in page.items],
            total_items=page.total_items,
            page=page.page,
            page_size=page.page_size,
        )
