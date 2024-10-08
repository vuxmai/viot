from datetime import datetime
from typing import Annotated
from uuid import UUID

from classy_fastapi import delete, get
from fastapi import Path, Query
from injector import inject

from app.common.controller import Controller
from app.common.dto.types import OrderByQuery, PageQuery, PageSizeQuery
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession
from app.module.auth.dependency import RequireTeamPermission
from app.module.auth.permission import TeamDeviceConnectLogPermission

from ..dto.connect_log_dto import PagingConnectLogDto
from ..service.connect_log_service import ConnectLogService


class ConnectLogController(Controller):
    @inject
    def __init__(self, connect_log_service: ConnectLogService) -> None:
        super().__init__(
            prefix="/teams/{team_id}/devices/{device_id}/connect-logs",
            tags=["Device Connect Logs"],
            dependencies=[DependSession],
        )
        self._connect_log_service = connect_log_service

    @get(
        "",
        summary="Get connect logs for a device",
        status_code=200,
        responses={200: {"model": PagingConnectLogDto}},
        dependencies=[RequireTeamPermission(TeamDeviceConnectLogPermission.READ)],
    )
    async def get_connect_logs(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        device_id: Annotated[UUID, Path(...)],
        page: PageQuery,
        page_size: PageSizeQuery,
        start_date: Annotated[datetime | None, Query(...)] = None,
        end_date: Annotated[datetime | None, Query(...)] = None,
        order_by: OrderByQuery,
    ) -> JSONResponse[PagingConnectLogDto]:
        """Get connect logs for a device."""
        return JSONResponse(
            content=await self._connect_log_service.get_connect_logs(
                team_id=team_id,
                device_id=device_id,
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date,
                order_by=order_by,
            ),
            status_code=200,
        )

    @delete(
        "",
        summary="Delete connect logs for a device",
        status_code=204,
        dependencies=[RequireTeamPermission(TeamDeviceConnectLogPermission.DELETE)],
    )
    async def delete_connect_logs(
        self,
        *,
        team_id: Annotated[UUID, Path(...)],
        device_id: Annotated[UUID, Path(...)],
        start_date: Annotated[datetime | None, Query(...)] = None,
        end_date: Annotated[datetime | None, Query(...)] = None,
    ) -> JSONResponse[None]:
        """Delete connect logs for a device."""
        await self._connect_log_service.delete_connect_logs(
            team_id=team_id,
            device_id=device_id,
            start_date=start_date,
            end_date=end_date,
        )
        return JSONResponse.no_content()
