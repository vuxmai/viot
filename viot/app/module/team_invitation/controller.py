from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, get, post
from fastapi.params import Body, Path
from injector import inject

from app.common.controller import Controller
from app.common.dto import PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.auth.dependency import DependCurrentUser
from app.module.team.constant import TeamRole
from app.module.team.dependency import RequireAnyTeamRole
from app.module.user.model import User

from .dto import (
    PagingTeamInvitationDto,
    TeamInvitationAcceptDto,
    TeamInvitationCreateDto,
    TeamInvitationDeclineDto,
    TeamInvitationDto,
    TeamInvitationRevokeDto,
)
from .service import TeamInvitationService


class TeamInvitationController(Controller):
    @inject
    def __init__(self, team_invitation_service: TeamInvitationService):
        super().__init__(
            prefix="/teams",
            tags=["Team Invitations"],
            dependencies=[DependSession],
        )
        self._team_invitation_service = team_invitation_service

    @get(
        "/{team_id}/invitations",
        status_code=200,
        summary="Get all team invitations",
        responses={200: {"model": PagingTeamInvitationDto}},
    )
    async def get_all_team_invitations(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        page: PageQuery = 1,
        page_size: PageSizeQuery = 10,
    ) -> JSONResponse[PagingTeamInvitationDto]:
        """Get all team invitations"""
        team_invitations = await self._team_invitation_service.get_pageable_team_invitations(
            team_id=team_id, page=page, page_size=page_size
        )
        return JSONResponse(content=team_invitations, status_code=200)

    @post(
        "/{team_id}/invitations",
        summary="Create a team invitation",
        status_code=201,
        responses={201: {"model": TeamInvitationDto}},
        dependencies=[
            RequireAnyTeamRole({TeamRole.OWNER, TeamRole.ADMIN}),
        ],
    )
    async def create_team_invitation(
        self,
        *,
        current_user: Annotated[User, DependCurrentUser],
        team_invitation_create_dto: Annotated[TeamInvitationCreateDto, Body(...)],
        team_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[TeamInvitationDto]:
        """Create a team invitation"""
        invitation = await self._team_invitation_service.create_team_invitation(
            team_id=team_id,
            inviter=current_user,
            team_invitation_create_dto=team_invitation_create_dto,
        )
        return JSONResponse(content=invitation, status_code=201)

    @delete(
        "/{team_id}/invitations/revoke",
        status_code=204,
        summary="Revoke a team invitation",
        dependencies=[
            RequireAnyTeamRole({TeamRole.OWNER, TeamRole.ADMIN}),
        ],
    )
    async def revoke_team_invitation(
        self,
        *,
        team_invitation_revoke_dto: Annotated[TeamInvitationRevokeDto, Body(...)],
    ) -> JSONResponse[None]:
        """Revoke a team invitation"""
        await self._team_invitation_service.revoke_team_invitation(
            token=team_invitation_revoke_dto.token
        )
        return JSONResponse.no_content()

    @post(
        "/invitations/accept",
        status_code=204,
        summary="Accept a team invitation",
        dependencies=[DependCurrentUser],
    )
    async def accept_team_invitation(
        self,
        *,
        team_invitation_accept_dto: Annotated[TeamInvitationAcceptDto, Body(...)],
    ) -> JSONResponse[None]:
        """Get a team invitation"""
        await self._team_invitation_service.accept_team_invitation(
            token=team_invitation_accept_dto.token
        )
        return JSONResponse.no_content()

    @delete(
        "/invitations/decline",
        status_code=204,
        summary="Decline a team invitation",
        dependencies=[DependCurrentUser],
    )
    async def decline_team_invitation(
        self,
        *,
        team_invitation_decline_dto: Annotated[TeamInvitationDeclineDto, Body(...)],
    ) -> JSONResponse[None]:
        """Decline a team invitation"""
        await self._team_invitation_service.decline_team_invitation(
            token=team_invitation_decline_dto.token
        )
        return JSONResponse.no_content()
