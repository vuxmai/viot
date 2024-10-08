from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.device_data.constants import AggregationType, IntervalType
from app.module.device_data.dto.device_data_dto import AggregatedData, TimeseriesAggregationQueryDto
from app.module.device_data.service.device_data_service import DeviceDataService


@pytest.fixture
def mock_device_data_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_device_data_latest_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_device_data_aggregation_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def device_data_service(
    mock_device_data_repository: AsyncMock,
    mock_device_data_latest_repository: AsyncMock,
    mock_device_data_aggregation_repository: AsyncMock,
) -> DeviceDataService:
    return DeviceDataService(
        device_data_repository=mock_device_data_repository,
        device_data_latest_repository=mock_device_data_latest_repository,
        device_data_aggregation_repository=mock_device_data_aggregation_repository,
    )


async def test_get_all_keys(
    device_data_service: DeviceDataService,
    mock_device_data_latest_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    mock_device_data_latest_repository.find_all_keys_by_device_id.return_value = [
        "key1",
        "key2",
    ]

    # when
    result = await device_data_service.get_all_keys(device_id=device_id)

    # then
    assert result == {"key1", "key2"}


async def test_get_latest_data_by_keys(
    device_data_service: DeviceDataService,
    mock_device_data_latest_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    keys = {"key1", "key2"}
    mock_device_data_latest_repository.find_all_by_device_id_and_keys.return_value = [
        Mock(device_id=device_id, key="key1", value=1, ts=datetime.now()),
        Mock(device_id=device_id, key="key2", value=2, ts=datetime.now()),
    ]

    # when
    result = await device_data_service.get_latest_data_by_keys(
        device_id=device_id,
        keys=keys,
    )

    # then
    assert len(result) == 2
    assert result[0].key == "key1"
    assert result[0].value == 1
    assert result[1].key == "key2"
    assert result[1].value == 2


async def test_get_timeseries_data_by_keys_without_aggregate(
    device_data_service: DeviceDataService,
    mock_device_data_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=10,
        orderBy="desc",
        timezone=None,
        intervalType=None,
        interval=0,
        agg=None,
    )
    mock_device_data_repository.find_data_by_device_id_and_keys.return_value = [
        Mock(device_id=device_id, key="key1", value=1, ts=datetime.now()),
        Mock(device_id=device_id, key="key2", value=2, ts=datetime.now()),
    ]

    # when
    result = await device_data_service.get_timeseries_data_by_keys(
        device_id=device_id,
        query_dto=query_dto,
    )

    # then
    assert len(result) == 2
    assert len(result["key1"]) == 1
    assert result["key1"][0].value == 1
    assert len(result["key2"]) == 1
    assert result["key2"][0].value == 2


async def test_get_timeseries_data_by_keys_with_aggregate(
    device_data_service: DeviceDataService,
    mock_device_data_aggregation_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=0,
        orderBy=None,
        timezone=None,
        intervalType=IntervalType.DAY,
        interval=1,
        agg=AggregationType.AVG,
    )
    mock_device_data_aggregation_repository.find_aggregation.return_value = [
        AggregatedData(ts=datetime.now(), value=1),
        AggregatedData(ts=datetime.now(), value=2),
    ]

    # when
    result = await device_data_service.get_timeseries_data_by_keys(
        device_id=device_id,
        query_dto=query_dto,
    )

    # then
    assert len(result) == 2
    assert len(result["key1"]) == 2
    assert result["key1"][0].value == 1
    assert result["key2"][1].value == 2
    assert len(result["key2"]) == 2
    assert result["key2"][0].value == 1
    assert result["key2"][1].value == 2


async def test_find_aggregation_async(
    device_data_service: DeviceDataService,
    mock_device_data_aggregation_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=0,
        orderBy=None,
        timezone=None,
        intervalType=IntervalType.DAY,
        interval=1,
        agg=AggregationType.AVG,
    )
    mock_device_data_aggregation_repository.find_aggregation.return_value = [
        AggregatedData(ts=datetime.now(), value=1),
        AggregatedData(ts=datetime.now(), value=2),
    ]

    # when
    result = await device_data_service.find_aggregation_async(
        device_id=device_id,
        query_dto=query_dto,
    )

    # then
    assert len(result) == 2
    assert result["key1"][0].value == 1
    assert result["key2"][1].value == 2
    assert len(result["key2"]) == 2
    assert result["key2"][0].value == 1
    assert result["key2"][1].value == 2


async def test_find_aggregation_raise_value_error_missing_agg(
    device_data_service: DeviceDataService,
) -> None:
    # given
    device_id = uuid4()
    # When using aggregation query, intervalType, interval and agg must be set
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=0,
        orderBy=None,
        timezone=None,
        intervalType=IntervalType.DAY,
        interval=1,
        agg=None,  # missing agg
    )

    # when
    with pytest.raises(ValueError):
        await device_data_service.find_aggregation_async(
            device_id=device_id,
            query_dto=query_dto,
        )


async def test_find_aggregation_raise_value_error_missing_interval_type(
    device_data_service: DeviceDataService,
) -> None:
    # given
    device_id = uuid4()
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=0,
        orderBy=None,
        timezone=None,
        intervalType=None,  # missing intervalType
        interval=1,
        agg=AggregationType.AVG,
    )

    # when
    with pytest.raises(ValueError):
        await device_data_service.find_aggregation_async(
            device_id=device_id,
            query_dto=query_dto,
        )


async def test_find_aggregation_raise_value_error_missing_interval(
    device_data_service: DeviceDataService,
) -> None:
    # given
    device_id = uuid4()
    query_dto = TimeseriesAggregationQueryDto(
        keys="key1,key2",
        startDate=str(datetime.now()),  # type: ignore
        endDate=str(datetime.now()),  # type: ignore
        limit=0,
        orderBy=None,
        timezone=None,
        intervalType=IntervalType.DAY,
        interval=0,  # interval must be greater than 0
        agg=AggregationType.AVG,
    )

    # when
    with pytest.raises(ValueError):
        await device_data_service.find_aggregation_async(
            device_id=device_id,
            query_dto=query_dto,
        )
