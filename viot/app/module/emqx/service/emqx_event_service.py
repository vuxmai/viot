import logging
from typing import Literal, TypedDict
from uuid import UUID

from httpx import AsyncClient, BasicAuth
from injector import inject

from app.module.device_data.constants import ConnectStatus
from app.module.device_data.model.connect_log import ConnectLog
from app.module.device_data.repository.connect_log_repository import ConnectLogRepository

from ..config import emqx_settings
from ..dto.emqx_event_dto import DeviceConnectedEventDto, DeviceDisconnectedEventDto


class Subscription(TypedDict):
    topic: str
    qos: Literal[0, 1, 2]
    nl: Literal[0, 1]
    rap: Literal[0, 1]
    rh: Literal[0, 1, 2]


logger = logging.getLogger(__name__)


class EmqxEventService:
    @inject
    def __init__(self, connect_log_repository: ConnectLogRepository) -> None:
        self._connect_log_repository = connect_log_repository

    async def handle_device_connected(self, *, event: DeviceConnectedEventDto) -> None:
        logger.info(f"Device connected with id: {event.device_id}")

        await self._subscribe_device_topics(event.device_id)

    async def handle_device_disconnected(self, *, event: DeviceDisconnectedEventDto) -> None:
        logger.info(f"Device disconnected with id: {event.device_id}, ip: {event.ip_address}")

        await self._connect_log_repository.save(
            ConnectLog(
                ts=event.disconnected_at,
                device_id=event.device_id,
                connect_status=ConnectStatus.DISCONNECTED,
                ip=event.ip_address,
            )
        )

    async def _subscribe_device_topics(self, device_id: UUID) -> None:
        async with AsyncClient(
            auth=BasicAuth(emqx_settings.API_KEY, emqx_settings.SECRET_KEY)
        ) as client:
            url: str = f"{emqx_settings.API_URL}/clients/{device_id}/subscribe/bulk"

            topics: list[Subscription] = [
                # Subscription(topic="test/2/xx", qos=0, nl=0, rap=0, rh=0),
                # Subscription(topic="test/3/xx", qos=0, nl=0, rap=0, rh=0),
            ]

            await client.post(url, json=topics)
