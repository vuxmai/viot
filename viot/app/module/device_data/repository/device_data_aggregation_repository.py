from collections.abc import Callable, Sequence
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import Row, text

from app.database.repository import AsyncSqlalchemyRepository

from ..constants import AggregationType, Timezone
from ..dto.device_data_dto import AggregatedData
from ..mapper import AggregatedDataMapper
from ..sql_queries import (
    FIND_AVG_QUERY,
    FIND_COUNT_QUERY,
    FIND_MAX_QUERY,
    FIND_MIN_QUERY,
    FIND_SUM_QUERY,
    FROM_WHERE_CLAUSE,
)

QUERY_MAP: dict[AggregationType, str] = {
    AggregationType.AVG: FIND_AVG_QUERY,
    AggregationType.MAX: FIND_MAX_QUERY,
    AggregationType.MIN: FIND_MIN_QUERY,
    AggregationType.SUM: FIND_SUM_QUERY,
    AggregationType.COUNT: FIND_COUNT_QUERY,
}
CONVERT_METHOD_MAP: dict[AggregationType, Callable[[Sequence[Row[Any]]], list[AggregatedData]]] = {
    AggregationType.AVG: AggregatedDataMapper.map_from_avg_rows,
    AggregationType.MAX: AggregatedDataMapper.map_from_max_rows,
    AggregationType.MIN: AggregatedDataMapper.map_from_min_rows,
    AggregationType.SUM: AggregatedDataMapper.map_from_sum_rows,
    AggregationType.COUNT: AggregatedDataMapper.map_from_count_rows,
}


class DeviceDataAggregationRepository(AsyncSqlalchemyRepository):
    async def find_aggregation(
        self,
        *,
        aggregation_type: AggregationType,
        device_id: UUID,
        key: str,
        start_date: datetime,
        end_date: datetime,
        bucket_width: timedelta,
        timezone: Timezone,
    ) -> list[AggregatedData]:
        query = QUERY_MAP[aggregation_type]
        convert_method = CONVERT_METHOD_MAP[aggregation_type]

        return await self._execute(
            query,
            {
                "device_id": device_id,
                "key": key,
                "start_date": start_date,
                "end_date": end_date,
                "bucket_width": bucket_width,
                "timezone": timezone,
            },
            convert_method,
        )

    async def _execute(
        self,
        query: str,
        params: dict[str, Any],
        convert_method: Callable[[Sequence[Row[Any]]], list[AggregatedData]],
    ) -> list[AggregatedData]:
        stmt = text(query + FROM_WHERE_CLAUSE)
        rows = (await self.session.execute(stmt, params)).fetchall()
        return convert_method(rows)
