from classy_fastapi import get
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession

from ..dependency import RequireTeamPermission
from ..dto.permission_dto import PermissionDto
from ..permission import TeamRolePermission
from ..service.permission_service import PermissionService


class PermissionController(Controller):
    @inject
    def __init__(self, permission_service: PermissionService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/permissions",
            tags=["Team Permissions"],
            dependencies=[DependSession],
        )
        self._permission_service = permission_service

    @get(
        "",
        summary="Get all permissions",
        status_code=200,
        responses={200: {"model": list[PermissionDto]}},
        dependencies=[RequireTeamPermission(TeamRolePermission.READ)],
    )
    async def get_all_permissions(self) -> JSONResponse[list[PermissionDto]]:
        """Get all permissions"""
        return JSONResponse(
            content=await self._permission_service.get_all_permissions(),
            status_code=200,
        )
