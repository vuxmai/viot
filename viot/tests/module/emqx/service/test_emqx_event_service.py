from datetime import UTC, datetime
from unittest import mock
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.module.emqx.config import emqx_settings
from app.module.emqx.dto.emqx_event_dto import DeviceConnectedEventDto, DeviceDisconnectedEventDto
from app.module.emqx.service.emqx_event_service import EmqxEventService


@pytest.fixture
def mock_connect_log_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def emqx_event_service(mock_connect_log_repository: AsyncMock) -> EmqxEventService:
    return EmqxEventService(connect_log_repository=mock_connect_log_repository)


async def test_handle_device_connected(emqx_event_service: EmqxEventService):
    # given
    device_id = uuid4()
    event = DeviceConnectedEventDto(device_id=device_id)
    emqx_event_service._subscribe_device_topics = AsyncMock()  # type: ignore

    # when
    await emqx_event_service.handle_device_connected(event=event)

    # then
    emqx_event_service._subscribe_device_topics.assert_called_once_with(device_id)  # type: ignore


async def test_handle_device_disconnected(
    emqx_event_service: EmqxEventService, mock_connect_log_repository: AsyncMock
):
    # given
    device_id = uuid4()
    ip_address = "192.168.1.1"
    event = DeviceDisconnectedEventDto(
        device_id=device_id, ip_address=ip_address, disconnected_at=datetime.now(UTC)
    )

    # when
    await emqx_event_service.handle_device_disconnected(event=event)

    # then
    mock_connect_log_repository.save.assert_awaited_once()


async def test_subscribe_device_topics(emqx_event_service: EmqxEventService):
    device_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    # Mocking AsyncClient and its post method
    with mock.patch("app.module.emqx.service.emqx_event_service.AsyncClient") as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock()

        await emqx_event_service._subscribe_device_topics(device_id)  # type: ignore

        # Check that the post method was called with the correct URL and topics
        url = f"{emqx_settings.API_URL}/clients/{device_id}/subscribe/bulk"
        mock_instance.post.assert_awaited_once_with(url, json=[])
