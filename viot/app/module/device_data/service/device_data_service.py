import asyncio
from collections import defaultdict
from uuid import UUID

from injector import inject

from ..constants import Timezone
from ..dto.device_data_dto import (
    AggregatedData,
    DataPointDto,
    LatestDataPointDto,
    TimeseriesAggregationQueryDto,
)
from ..repository.device_data_aggregation_repository import DeviceDataAggregationRepository
from ..repository.device_data_latest_repository import DeviceDataLatestRepository
from ..repository.device_data_repository import DeviceDataRepository


class DeviceDataService:
    @inject
    def __init__(
        self,
        device_data_repository: DeviceDataRepository,
        device_data_latest_repository: DeviceDataLatestRepository,
        device_data_aggregation_repository: DeviceDataAggregationRepository,
    ) -> None:
        self._device_data_repository = device_data_repository
        self._device_data_latest_repository = device_data_latest_repository
        self._device_data_aggregation_repository = device_data_aggregation_repository

    async def get_all_keys(self, *, device_id: UUID) -> set[str]:
        keys = await self._device_data_latest_repository.find_all_keys_by_device_id(
            device_id=device_id
        )
        return set(keys)

    async def get_latest_data_by_keys(
        self, *, device_id: UUID, keys: set[str]
    ) -> list[LatestDataPointDto]:
        data = await self._device_data_latest_repository.find_all_by_device_id_and_keys(
            device_id=device_id, keys=keys
        )
        return [LatestDataPointDto.from_model(d) for d in data]

    async def get_timeseries_data_by_keys(
        self, *, device_id: UUID, query_dto: TimeseriesAggregationQueryDto
    ) -> dict[str, list[DataPointDto]]:
        result_map: defaultdict[str, list[DataPointDto]] = defaultdict(list)

        if not query_dto.is_aggregate_query:
            data = await self._device_data_repository.find_data_by_device_id_and_keys(
                device_id=device_id,
                keys=query_dto.keys,
                start_date=query_dto.start_date,
                end_date=query_dto.end_date,
                limit=query_dto.limit,
                order_by=query_dto.order_by,
            )

            for i in data:
                result_map[i.key].append(DataPointDto.from_model(i))
        else:
            aggregated_data = await self.find_aggregation_async(device_id, query_dto)
            for key, values in aggregated_data.items():
                result_map[key].extend([DataPointDto.from_model(v) for v in values])

        return result_map

    async def find_aggregation_async(
        self, device_id: UUID, query_dto: TimeseriesAggregationQueryDto
    ) -> dict[str, list[AggregatedData]]:
        if not query_dto.is_aggregate_query:
            raise ValueError("Query is not an aggregation query")

        results = await asyncio.gather(
            *[
                self._device_data_aggregation_repository.find_aggregation(
                    aggregation_type=query_dto.agg,  # type: ignore
                    device_id=device_id,
                    key=key,
                    start_date=query_dto.start_date,
                    end_date=query_dto.end_date,
                    bucket_width=query_dto.interval_in_timedelta,
                    timezone=query_dto.timezone or Timezone.UTC,
                )
                for key in query_dto.keys
            ]
        )

        return dict(zip(query_dto.keys, results, strict=True))
