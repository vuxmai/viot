from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from pytest import approx  # type: ignore

from app.module.device_data.dto.device_data_dto import AggregatedData
from app.module.device_data.mapper import AggregatedDataMapper


@pytest.fixture
def mock_sample_row() -> Mock:
    return Mock(
        bucket=datetime(2023, 1, 1),
        interval=timedelta(seconds=3600),
        long_value=10,
        double_value=5.5,
        count_long_value=2,
        count_double_value=1,
        count_bool_value=0,
        count_str_value=0,
        count_json_value=0,
    )


def test_map_from_avg_rows(mock_sample_row: Mock) -> None:
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_avg_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == approx(15.5 / 3)


def test_map_from_avg_rows_total_count_zero(mock_sample_row: Mock) -> None:
    mock_sample_row.count_long_value = 0
    mock_sample_row.count_double_value = 0
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_avg_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == approx(0.0)


def test_map_from_sum_rows(mock_sample_row: Mock) -> None:
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_sum_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == approx(15.5)


def test_map_from_min_rows(mock_sample_row: Mock) -> None:
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_min_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == approx(5.5)


def test_map_from_max_rows(mock_sample_row: Mock) -> None:
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_max_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == 10


def test_map_from_count_rows(mock_sample_row: Mock) -> None:
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_count_rows(rows)
    assert len(result) == 1
    assert isinstance(result[0], AggregatedData)
    assert result[0].ts == datetime(2023, 1, 1, 0, 30)
    assert result[0].value == 3


def test_map_from_count_rows_with_bool_value(mock_sample_row: Mock) -> None:
    mock_sample_row.count_bool_value = 5
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_count_rows(rows)
    assert len(result) == 1
    assert result[0].value == 5


def test_map_from_count_rows_with_str_value(mock_sample_row: Mock) -> None:
    mock_sample_row.count_str_value = 7
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_count_rows(rows)
    assert len(result) == 1
    assert result[0].value == 7


def test_map_from_count_rows_with_json_value(mock_sample_row: Mock) -> None:
    mock_sample_row.count_json_value = 9
    rows = [mock_sample_row]
    result = AggregatedDataMapper.map_from_count_rows(rows)
    assert len(result) == 1
    assert result[0].value == 9
