from uuid import UUID

from app.common.exception import PermissionDeniedException, UnauthorizedException


class DeviceCredentialException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_DEVICE_CREDENTIAL",
            message="Invalid device credential",
        )


class DeviceDisabledException(PermissionDeniedException):
    def __init__(self, device_id: UUID) -> None:
        super().__init__(
            code="DEVICE_DISABLED",
            message=f"Device with id {device_id} is disabled",
        )
