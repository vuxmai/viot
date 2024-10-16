import logging
from datetime import UTC, datetime

from injector import inject

from app.module.device.constants import DeviceStatus
from app.module.device.exception.device_exception import DeviceNotFoundException
from app.module.device.model.device import Device
from app.module.device.repository.device_repository import DeviceRepository
from app.module.device_data.constants import ConnectStatus
from app.module.device_data.model.connect_log import ConnectLog
from app.module.device_data.repository.connect_log_repository import ConnectLogRepository

from ..dto.emqx_auth_dto import EmqxAuthenRequestDto, EmqxAuthenResponseDto
from ..exception.emqx_auth_exception import DeviceCredentialException, DeviceDisabledException
from ..service.mqtt_whitelist_service import MqttWhitelistService

logger = logging.getLogger(__name__)


class EmqxDeviceAuthService:
    @inject
    def __init__(
        self,
        device_repository: DeviceRepository,
        connect_log_repository: ConnectLogRepository,
        mqtt_whitelist_service: MqttWhitelistService,
    ) -> None:
        self._device_repository = device_repository
        self._connect_log_repository = connect_log_repository
        self._mqtt_whitelist_service = mqtt_whitelist_service

    async def authenticate(self, *, request_dto: EmqxAuthenRequestDto) -> EmqxAuthenResponseDto:
        logger.info(
            f"Authenticating device with id {request_dto.device_id}, ip {request_dto.ip_address}"
        )

        last_connection = datetime.now(UTC)
        connect_status = ConnectStatus.FAILED
        device: Device | None = None

        # Check if the device is in the whitelist
        if self._mqtt_whitelist_service.check_is_in_whitelist(
            request_dto.device_id, request_dto.password
        ):
            return EmqxAuthenResponseDto(result="allow", is_superuser=True)

        try:
            device = await self._device_repository.find(request_dto.device_id)
            if device is None:
                raise DeviceNotFoundException(request_dto.device_id)

            # Validate credentials
            if device.token != request_dto.password and device.token != request_dto.username:
                raise DeviceCredentialException

            # Check if the device is disabled
            if device.disabled:
                raise DeviceDisabledException(device.id)

            # Update device info
            device.last_connection = last_connection
            device.status = DeviceStatus.ONLINE
            connect_status = ConnectStatus.CONNECTED  # Successful connection

            return EmqxAuthenResponseDto(
                result="allow",
                is_superuser=False,
                acl=[
                    # {
                    #     "permission": "allow",
                    #     "action": "all",
                    #     "topic": "eq test/1/#",
                    # },
                    # {
                    #     "permission": "allow",
                    #     "action": "all",
                    #     "topic": "test/2/#",
                    # },
                ],
            )

        except (DeviceNotFoundException, DeviceCredentialException, DeviceDisabledException) as e:
            # Re-raise exception
            raise e

        finally:
            # Save connection log (for both success and failure)

            # TODO: Run in background or may be event emitter
            if device:
                await self._connect_log_repository.save(
                    ConnectLog(
                        ts=last_connection,
                        device_id=request_dto.device_id,
                        connect_status=connect_status,
                        ip=request_dto.ip_address,
                    )
                )