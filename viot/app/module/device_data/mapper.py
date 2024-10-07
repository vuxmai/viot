from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row

from .dto.device_data_dto import AggregatedData


class AggregatedDataMapper:
    @staticmethod
    def map_from_avg_rows(rows: Sequence[Row[Any]]) -> list[AggregatedData]:
        data: list[AggregatedData] = []

        for row in rows:
            sum: float = 0.0

            if row.long_value:
                sum += row.long_value
            if row.double_value:
                sum += row.double_value

            total_count: int = row.count_long_value + row.count_double_value

            if total_count > 0:
                avg = sum / total_count
            else:
                avg = 0.0

            data.append(AggregatedData(ts=row.bucket + row.interval / 2, value=avg))

        return data

    @staticmethod
    def map_from_sum_rows(rows: Sequence[Row[Any]]) -> list[AggregatedData]:
        data: list[AggregatedData] = []

        for row in rows:
            sum: float = 0.0

            if row.long_value:
                sum += row.long_value
            if row.double_value:
                sum += row.double_value

            data.append(AggregatedData(ts=row.bucket + row.interval / 2, value=sum))

        return data

    @staticmethod
    def map_from_min_rows(rows: Sequence[Row[Any]]) -> list[AggregatedData]:
        data: list[AggregatedData] = []

        for row in rows:
            min_value = min(row.long_value, row.double_value)
            data.append(AggregatedData(ts=row.bucket + row.interval / 2, value=min_value))

        return data

    @staticmethod
    def map_from_max_rows(rows: Sequence[Row[Any]]) -> list[AggregatedData]:
        data: list[AggregatedData] = []

        for row in rows:
            max_value = max(row.long_value, row.double_value)
            data.append(AggregatedData(ts=row.bucket + row.interval / 2, value=max_value))

        return data

    @staticmethod
    def map_from_count_rows(rows: Sequence[Row[Any]]) -> list[AggregatedData]:
        data: list[AggregatedData] = []
        total_count: int = 0

        for row in rows:
            if row.count_bool_value != 0:
                total_count = row.count_bool_value
            elif row.count_str_value != 0:
                total_count = row.count_str_value
            elif row.count_json_value != 0:
                total_count = row.count_json_value
            else:
                total_count = row.count_long_value + row.count_double_value

            data.append(AggregatedData(ts=row.bucket + row.interval / 2, value=total_count))

        return data
