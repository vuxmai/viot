import re
from datetime import datetime
from typing import Annotated, Any

from fastapi import Depends, Query

from app.common.dto import BaseOutDto

from ..model.device_data import DeviceData
from ..model.device_data_latest import DeviceDataLatest


def keys_comma_separated_values(
    value: str = Query(
        alias="keys",
        description="A string value representing the comma-separated list of telemetry keys.",
        example="kWh,temperature,humidity",
    ),
) -> set[str]:
    result = re.split(r"\s*,\s*", value)
    result = {item for item in result if item}
    if not result:
        raise ValueError("At least one key is required")
    return result


def start_date_value(
    value: datetime = Query(
        alias="startDate",
        description=(
            "A string value representing the start date in ISO format,"
            " any timezone will be removed."
        ),
        example="2021-01-01T00:00:00",
    ),
) -> datetime:
    return value.replace(tzinfo=None)


def end_date_value(
    value: datetime = Query(
        alias="endDate",
        description=(
            "A string value representing the end date in ISO format,"
            " any timezone will be removed."
        ),
        example="2022-01-01T00:00:00",
    ),
) -> datetime:
    return value.replace(tzinfo=None)


KeySetQuery = Annotated[set[str], Depends(keys_comma_separated_values)]


class DeviceDataDto(BaseOutDto):
    ts: datetime
    key: str
    value: Any

    @classmethod
    def from_model(cls, model: DeviceData | DeviceDataLatest) -> "DeviceDataDto":
        return cls(ts=model.ts, key=model.key, value=model.value)
