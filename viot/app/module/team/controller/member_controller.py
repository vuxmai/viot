from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, get, patch
from fastapi import Query
from fastapi.params import Path
from injector import inject

from app.common.controller import Controller
from app.common.dto.types import PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.database.repository.pagination import SortDirection
from app.module.auth.dependency import RequireTeamPermission
from app.module.auth.permission import TeamMemberPermission

from ..dto.member_dto import MemberDto, MemberPagingDto, MemberUpdateDto
from ..service.member_service import MemberService


class MemberController(Controller):
    @inject
    def __init__(self, member_service: MemberService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/members", tags=["Team Members"], dependencies=[DependSession]
        )
        self._member_service = member_service

    @get(
        "",
        summary="Get paging members",
        status_code=200,
        responses={200: {"model": MemberPagingDto}},
        dependencies=[RequireTeamPermission(TeamMemberPermission.READ)],
    )
    async def get_paging_members(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        page: PageQuery,
        page_size: PageSizeQuery,
        joined_at: Annotated[SortDirection, Query(alias="joinedAt")],
    ) -> JSONResponse[MemberPagingDto]:
        """Get paging members"""
        return JSONResponse(
            content=await self._member_service.find_paging_members(
                team_id=team_id,
                page=page,
                page_size=page_size,
                sort_direction_joined_at=joined_at,
            ),
            status_code=200,
        )

    @get(
        "/{member_id}",
        summary="Get member by id",
        status_code=200,
        responses={200: {"model": MemberDto}},
        dependencies=[RequireTeamPermission(TeamMemberPermission.READ)],
    )
    async def get_member_by_id(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        member_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[MemberDto]:
        """Get member by id"""
        return JSONResponse(
            content=await self._member_service.get_member_by_id_and_team_id(
                team_id=team_id, member_id=member_id
            ),
            status_code=200,
        )

    @patch(
        "/{member_id}",
        summary="Update member by id",
        status_code=200,
        responses={200: {"model": MemberDto}},
        dependencies=[RequireTeamPermission(TeamMemberPermission.MANAGE)],
    )
    async def update_member_by_id(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        member_id: Annotated[UUID, Path(...)],
        member_update_dto: MemberUpdateDto,
    ) -> JSONResponse[MemberDto]:
        """Update member by id"""
        return JSONResponse(
            content=await self._member_service.update_member(
                team_id=team_id, member_id=member_id, member_update_dto=member_update_dto
            ),
            status_code=200,
        )

    @delete(
        "/{member_id}",
        summary="Delete member by id",
        status_code=204,
        dependencies=[RequireTeamPermission(TeamMemberPermission.DELETE)],
    )
    async def delete_member_by_id(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        member_id: Annotated[UUID, Path(...)],
    ) -> None:
        """Delete member by id"""
        await self._member_service.delete_member(team_id=team_id, member_id=member_id)
