import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from injector import inject

from app.config import app_settings
from app.database.repository import Filter, Pageable
from app.module.auth.exception.user_exception import UserNotFoundException
from app.module.auth.model.user import User
from app.module.auth.repository.user_repository import UserRepository
from app.module.email.service import IEmailService

from ..constants import INVITATION_EXPIRATION_DAYS
from ..dto.team_invitation_dto import (
    PagingTeamInvitationDto,
    TeamInvitationCreateDto,
    TeamInvitationDto,
)
from ..exception.team_exception import TeamNotFoundException
from ..exception.team_invitation_exception import (
    TeamInvitationExpiredException,
    TeamInvitationNotFoundException,
)
from ..model.team_invitation import TeamInvitation
from ..model.user_team import UserTeam
from ..repository.team_invitation_repository import TeamInvitationRepository
from ..repository.team_repository import TeamRepository
from ..repository.user_team_repository import UserTeamRepository

logger = logging.getLogger(__name__)


class TeamInvitationService:
    @inject
    def __init__(
        self,
        email_service: IEmailService,
        user_repository: UserRepository,
        team_repository: TeamRepository,
        user_team_repository: UserTeamRepository,
        team_invitation_repository: TeamInvitationRepository,
    ) -> None:
        self._email_service = email_service
        self._user_repository = user_repository
        self._team_repository = team_repository
        self._user_team_repository = user_team_repository
        self._team_invitation_repository = team_invitation_repository

    async def get_pageable_team_invitations(
        self, team_id: UUID, page: int, page_size: int
    ) -> PagingTeamInvitationDto:
        pageable = Pageable(
            page=page,
            page_size=page_size,
            filters=[Filter(field="team_id", operator="eq", value=team_id)],
        )
        team_invitation_page = await self._team_invitation_repository.find_all_with_paging(pageable)
        return PagingTeamInvitationDto.from_page(team_invitation_page)

    async def create_team_invitation(
        self, *, team_id: UUID, inviter: User, team_invitation_create_dto: TeamInvitationCreateDto
    ) -> TeamInvitationDto:
        invitee = await self._user_repository.find_by_email(team_invitation_create_dto.email)
        if invitee is None:
            raise UserNotFoundException

        team = await self._team_repository.find(team_id)
        if team is None:
            raise TeamNotFoundException

        invitation = await self._team_invitation_repository.save(
            TeamInvitation(
                inviter_id=inviter.id,
                team_id=team_id,
                email=team_invitation_create_dto.email,
                role=team_invitation_create_dto.role,
            )
        )

        self._email_service.send_team_invitation_email(
            email=invitee.email,
            name=invitee.first_name,
            invitor_name=inviter.first_name,
            team_name=team.name,
            link=f"{app_settings.UI_URL}/{team.slug}/invitations?token={invitation.token}",
        )
        return TeamInvitationDto.from_model(invitation)

    async def accept_team_invitation(self, *, token: str) -> None:
        invitation = await self._team_invitation_repository.find_by_token(token)
        if invitation is None:
            raise TeamInvitationNotFoundException

        if invitation.created_at < datetime.now(UTC) - timedelta(days=INVITATION_EXPIRATION_DAYS):
            raise TeamInvitationExpiredException

        invitee_id = await self._user_repository.find_id_by_email(invitation.email)
        if invitee_id is None:
            logger.warning(f"Invitation accepted by non-existent user: {invitation.email}")
            await self._team_invitation_repository.delete(invitation)
            return

        await self._user_team_repository.save(
            UserTeam(user_id=invitee_id, team_id=invitation.team_id, role=invitation.role)
        )
        await self._team_invitation_repository.delete(invitation)

    async def decline_team_invitation(self, *, token: str) -> None:
        await self._delete_team_invitation_by_token(token)

    async def revoke_team_invitation_by_id(self, *, id: UUID) -> None:
        invitation = await self._team_invitation_repository.find(id)
        if invitation is None:
            raise TeamInvitationNotFoundException

        await self._team_invitation_repository.delete(invitation)

    async def _delete_team_invitation_by_token(self, token: str) -> None:
        invitation = await self._team_invitation_repository.find_by_token(token)
        if invitation is None:
            raise TeamInvitationNotFoundException

        await self._team_invitation_repository.delete(invitation)
