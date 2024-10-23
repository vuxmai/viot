from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, get, post, put
from fastapi import Body, Path
from fastapi.params import Query
from injector import inject

from app.common.controller import Controller
from app.common.dto.types import PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.auth.dependency import RequireTeamPermission
from app.module.auth.permission import TeamRulePermission

from ..dto.rule_dto import RuleCreateDto, RulePagingDto, RuleResponseDto, RuleUpdateDto
from ..service.rule_service import RuleService


class RuleController(Controller):
    @inject
    def __init__(self, rule_service: RuleService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/rules",
            tags=["Rules & Actions"],
            dependencies=[DependSession],
        )
        self._rule_service = rule_service

    @get(
        "",
        summary="Get paging rules",
        status_code=200,
        responses={200: {"model": RulePagingDto}},
        dependencies=[RequireTeamPermission(TeamRulePermission.READ)],
    )
    async def get_paging_rules(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        page: PageQuery,
        page_size: PageSizeQuery,
        device_id: Annotated[UUID | None, Query(..., description="Filter by device id")] = None,
    ) -> JSONResponse[RulePagingDto]:
        """
        Get paging rules.
        """
        return JSONResponse(
            content=await self._rule_service.get_paging_rules(
                team_id=team_id, device_id=device_id, page=page, page_size=page_size
            ),
            status_code=200,
        )

    @get(
        "/{rule_id}",
        summary="Get rule by id",
        status_code=200,
        responses={200: {"model": RuleResponseDto}},
        dependencies=[RequireTeamPermission(TeamRulePermission.READ)],
    )
    async def get_rule_by_id(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        rule_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[RuleResponseDto]:
        """
        Get rule by id.
        """
        return JSONResponse(
            content=await self._rule_service.get_rule_by_id_and_team_id(
                team_id=team_id, rule_id=rule_id
            ),
            status_code=200,
        )

    @post(
        "",
        summary="Create a new rule",
        status_code=201,
        responses={201: {"model": RuleResponseDto}},
        dependencies=[RequireTeamPermission(TeamRulePermission.MANAGE)],
    )
    async def create_rule(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        body: Annotated[RuleCreateDto, Body(...)],
    ) -> JSONResponse[RuleResponseDto]:
        """
        Create a new rule.
        """
        return JSONResponse(
            content=await self._rule_service.create_rule(team_id=team_id, rule_create_dto=body),
            status_code=201,
        )

    @put(
        "/{rule_id}",
        summary="Update a rule",
        status_code=200,
        responses={200: {"model": RuleResponseDto}},
        dependencies=[RequireTeamPermission(TeamRulePermission.MANAGE)],
    )
    async def update_rule(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        rule_id: Annotated[UUID, Path(...)],
        body: Annotated[RuleUpdateDto, Body(...)],
    ) -> JSONResponse[RuleResponseDto]:
        """
        Update a rule.
        """
        return JSONResponse(
            content=await self._rule_service.update_rule(
                team_id=team_id, rule_id=rule_id, rule_update_dto=body
            ),
            status_code=200,
        )

    @delete(
        "/{rule_id}",
        summary="Delete a rule",
        status_code=204,
        dependencies=[RequireTeamPermission(TeamRulePermission.DELETE)],
    )
    async def delete_rule(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        rule_id: Annotated[UUID, Path(...)],
    ) -> JSONResponse[None]:
        """
        Delete a rule.
        """
        await self._rule_service.delete_rule(team_id=team_id, rule_id=rule_id)
        return JSONResponse.no_content()
