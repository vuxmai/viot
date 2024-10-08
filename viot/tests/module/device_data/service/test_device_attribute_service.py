from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.device_data.service.device_attribute_service import DeviceAttributeService


@pytest.fixture
def mock_device_attribute_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def device_attribute_service(
    mock_device_attribute_repository: AsyncMock,
) -> DeviceAttributeService:
    return DeviceAttributeService(
        device_attribute_repository=mock_device_attribute_repository,
    )


async def test_get_all_keys(
    device_attribute_service: DeviceAttributeService,
    mock_device_attribute_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    mock_device_attribute_repository.find_all_keys_by_device_id.return_value = [
        "key1",
        "key2",
    ]

    # when
    result = await device_attribute_service.get_all_keys(device_id=device_id)

    # then
    assert result == {"key1", "key2"}


async def test_get_all_by_device_id(
    device_attribute_service: DeviceAttributeService,
    mock_device_attribute_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    keys = {"key1", "key2"}
    mock_device_attribute_repository.find_all_by_device_id_and_keys.return_value = [
        Mock(key="key1", value="value1", last_update=datetime(2021, 1, 1), device_can_edit=True),
        Mock(key="key2", value="value2", last_update=datetime(2021, 1, 1), device_can_edit=True),
    ]

    # when
    result = await device_attribute_service.get_all_by_device_id(device_id=device_id, keys=keys)

    # then
    assert len(result) == 2
    assert result[0].key == "key1"
    assert result[0].value == "value1"
    assert result[0].last_update == datetime(2021, 1, 1)
    assert result[0].device_can_edit is True
    assert result[1].key == "key2"
    assert result[1].value == "value2"
    assert result[1].last_update == datetime(2021, 1, 1)
    assert result[1].device_can_edit is True
