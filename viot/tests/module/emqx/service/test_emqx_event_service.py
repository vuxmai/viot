from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.common.exception.base import InternalServerException
from app.module.emqx.config import emqx_settings
from app.module.emqx.dto.emqx_event_dto import DeviceConnectedEventDto, DeviceDisconnectedEventDto
from app.module.emqx.service.emqx_event_service import EmqxEventService


@pytest.fixture
def mock_connect_log_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def emqx_event_service(mock_connect_log_repository: AsyncMock) -> EmqxEventService:
    return EmqxEventService(connect_log_repository=mock_connect_log_repository)


async def test_handle_device_connected(emqx_event_service: EmqxEventService) -> None:
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
) -> None:
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


@patch("app.module.emqx.service.emqx_event_service.AsyncClient")
async def test_subscribe_device_topics(mock_async_client: AsyncMock) -> None:
    # given
    emqx_event_service = EmqxEventService(connect_log_repository=AsyncMock())
    device_id = uuid4()
    mock_response = mock_async_client.return_value.__aenter__.return_value.post.return_value
    mock_response.status_code = 201

    # when
    await emqx_event_service._subscribe_device_topics(device_id)  # type: ignore

    # then
    mock_async_client.return_value.__aenter__.return_value.post.assert_awaited_once_with(
        f"{emqx_settings.API_URL}/clients/{device_id}/subscribe/bulk", json=[]
    )


@patch("app.module.emqx.service.emqx_event_service.AsyncClient")
async def test_subscribe_device_topics_throws_exception_on_failure(
    mock_async_client: AsyncMock,
) -> None:
    # given
    emqx_event_service = EmqxEventService(connect_log_repository=AsyncMock())
    device_id = uuid4()
    mock_response = mock_async_client.return_value.__aenter__.return_value.post.return_value
    mock_response.status_code = 500

    # when / then
    with pytest.raises(InternalServerException, match="Error while subscribing to topics"):
        await emqx_event_service._subscribe_device_topics(device_id)  # type: ignore
