from datetime import datetime
from uuid import UUID

from injector import inject

from app.database.repository import Filter, Pageable, Sort
from app.database.repository.pagination import SortDirection
from app.module.device.exception.device_exception import DeviceNotFoundException
from app.module.device.repository.device_repository import DeviceRepository

from ..dto.connect_log_dto import PagingConnectLogDto
from ..repository.connect_log_repository import ConnectLogRepository


class ConnectLogService:
    @inject
    def __init__(
        self, connect_log_repository: ConnectLogRepository, device_repository: DeviceRepository
    ) -> None:
        self._connect_log_repository = connect_log_repository
        self._device_repository = device_repository

    async def get_connect_logs(
        self,
        *,
        team_id: UUID,
        device_id: UUID,
        page: int,
        page_size: int,
        start_date: datetime | None,
        end_date: datetime | None,
        order_by: SortDirection | None,
    ) -> PagingConnectLogDto:
        self._validate_date_range(start_date, end_date)
        await self._validate_team_and_device(team_id, device_id)

        filters = [Filter(field="device_id", operator="eq", value=device_id)]
        if start_date:
            filters.append(Filter(field="ts", operator="gte", value=start_date))
        if end_date:
            filters.append(Filter(field="ts", operator="lte", value=end_date))

        pageable = Pageable(page=page, page_size=page_size, filters=filters)

        if order_by:
            pageable.sorts.append(Sort(field="ts", direction=order_by))

        connect_log_page = await self._connect_log_repository.find_all_with_paging(pageable)
        return PagingConnectLogDto.from_page(connect_log_page)

    async def delete_connect_logs(
        self,
        *,
        team_id: UUID,
        device_id: UUID,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> None:
        self._validate_date_range(start_date, end_date)
        await self._validate_team_and_device(team_id, device_id)

        await self._connect_log_repository.delete_by_device_id_and_date_range(
            device_id=device_id, start_date=start_date, end_date=end_date
        )

    async def _validate_team_and_device(self, team_id: UUID, device_id: UUID) -> None:
        if not await self._device_repository.exists_by_id_and_team_id(device_id, team_id):
            raise DeviceNotFoundException(device_id)

    def _validate_date_range(self, start_date: datetime | None, end_date: datetime | None) -> None:
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date must be less than or equal to end_date")
