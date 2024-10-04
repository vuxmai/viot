from typing import Any
from uuid import UUID

from injector import inject
from sqlalchemy import func

from ..constants import AggregationType
from ..dto.device_data_dto import DeviceDataDto
from ..repository.device_data_latest_repository import DeviceDataLatestRepository
from ..repository.device_data_repository import DeviceDataRepository

AGGREGATION_FUNCTIONS_MAP: dict[AggregationType, Any] = {
    AggregationType.AVG: func.avg,
    AggregationType.SUM: func.sum,
    AggregationType.MIN: func.min,
    AggregationType.MAX: func.max,
    AggregationType.COUNT: func.count,
}


class DeviceDataService:
    @inject
    def __init__(
        self,
        device_data_repository: DeviceDataRepository,
        device_data_latest_repository: DeviceDataLatestRepository,
    ) -> None:
        self._device_data_repository = device_data_repository
        self._device_data_latest_repository = device_data_latest_repository

    async def get_all_keys(self, *, device_id: UUID) -> set[str]:
        keys = await self._device_data_latest_repository.find_all_keys_by_device_id(
            device_id=device_id
        )
        return set(keys)

    async def get_latest_data_by_keys(
        self, *, device_id: UUID, keys: set[str]
    ) -> list[DeviceDataDto]:
        data = await self._device_data_latest_repository.find_all_by_device_id_and_keys(
            device_id=device_id, keys=keys
        )
        return [DeviceDataDto.from_model(d) for d in data]
