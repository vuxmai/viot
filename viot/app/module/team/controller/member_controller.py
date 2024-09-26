from typing import Annotated
from uuid import UUID

from classy_fastapi import get
from fastapi import Query
from fastapi.params import Path
from injector import inject

from app.common.controller import Controller
from app.common.dto.types import PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.database.repository.pagination import SortDirection

from ..constants import TeamRole
from ..dependency import RequireAnyTeamRole
from ..dto.member_dto import MemberPagingDto
from ..service.member_service import MemberService


class MemberController(Controller):
    @inject
    def __init__(self, member_service: MemberService):
        super().__init__(
            prefix="/teams/{team_id}/members", tags=["Team Members"], dependencies=[DependSession]
        )
        self._member_service = member_service

    @get(
        "",
        summary="Get paging members",
        status_code=200,
        responses={200: {"model": MemberPagingDto}},
        dependencies=[RequireAnyTeamRole({TeamRole.OWNER, TeamRole.ADMIN, TeamRole.MEMBER})],
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
