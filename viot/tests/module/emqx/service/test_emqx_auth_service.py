from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.module.device.exception.device_exception import DeviceNotFoundException
from app.module.emqx.dto.emqx_auth_dto import EmqxAuthenRequestDto
from app.module.emqx.exception.emqx_auth_exception import (
    DeviceCredentialException,
    DeviceDisabledException,
)
from app.module.emqx.service.emqx_auth_service import EmqxDeviceAuthService


@pytest.fixture
def mock_device_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_connect_log_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_mqtt_whitelist_service() -> Mock:
    return Mock()


@pytest.fixture
def emqx_device_auth_service(
    mock_device_repository: AsyncMock,
    mock_connect_log_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
) -> EmqxDeviceAuthService:
    return EmqxDeviceAuthService(
        device_repository=mock_device_repository,
        connect_log_repository=mock_connect_log_repository,
        mqtt_whitelist_service=mock_mqtt_whitelist_service,
    )


@pytest.fixture
def emqx_authen_request_dto() -> EmqxAuthenRequestDto:
    return EmqxAuthenRequestDto(
        device_id=uuid4(),
        username="valid_token",
        password="valid_token",
        ip_address="192.168.1.1",
    )


async def test_authenticate_device_in_whitelist(
    emqx_device_auth_service: EmqxDeviceAuthService,
    mock_connect_log_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
    emqx_authen_request_dto: EmqxAuthenRequestDto,
) -> None:
    # given
    mock_mqtt_whitelist_service.check_is_in_whitelist = Mock(return_value=True)

    # when
    response = await emqx_device_auth_service.authenticate(request_dto=emqx_authen_request_dto)

    # then
    assert response.result == "allow"
    assert response.is_superuser is True

    # then
    mock_connect_log_repository.save.assert_not_called()


async def test_authenticate_device_not_found(
    emqx_device_auth_service: EmqxDeviceAuthService,
    mock_device_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
    emqx_authen_request_dto: EmqxAuthenRequestDto,
) -> None:
    # given
    mock_device_repository.find = AsyncMock(return_value=None)
    mock_mqtt_whitelist_service.check_is_in_whitelist = Mock(return_value=False)

    # when
    with pytest.raises(DeviceNotFoundException):
        await emqx_device_auth_service.authenticate(request_dto=emqx_authen_request_dto)


async def test_authenticate_device_credentials_invalid(
    emqx_device_auth_service: EmqxDeviceAuthService,
    mock_device_repository: AsyncMock,
    mock_connect_log_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
    emqx_authen_request_dto: EmqxAuthenRequestDto,
) -> None:
    # given
    mock_mqtt_whitelist_service.check_is_in_whitelist = Mock(return_value=False)
    mock_device_repository.find = AsyncMock(id=uuid4(), token="valid_token", disabled=False)

    # when
    with pytest.raises(DeviceCredentialException):
        await emqx_device_auth_service.authenticate(request_dto=emqx_authen_request_dto)

    # then
    mock_connect_log_repository.save.assert_called_once()


async def test_authenticate_device_disabled(
    emqx_device_auth_service: EmqxDeviceAuthService,
    mock_device_repository: AsyncMock,
    mock_connect_log_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
    emqx_authen_request_dto: EmqxAuthenRequestDto,
) -> None:
    # given
    mock_mqtt_whitelist_service.check_is_in_whitelist = Mock(return_value=False)
    mock_device_repository.find = AsyncMock(
        return_value=Mock(id=uuid4(), token="valid_token", disabled=True)
    )

    # when
    with pytest.raises(DeviceDisabledException):
        await emqx_device_auth_service.authenticate(request_dto=emqx_authen_request_dto)

    # then
    mock_connect_log_repository.save.assert_called_once()


async def test_authenticate_success(
    emqx_device_auth_service: EmqxDeviceAuthService,
    mock_device_repository: AsyncMock,
    mock_connect_log_repository: AsyncMock,
    mock_mqtt_whitelist_service: Mock,
    emqx_authen_request_dto: EmqxAuthenRequestDto,
) -> None:
    # given
    mock_mqtt_whitelist_service.check_is_in_whitelist = Mock(return_value=False)
    mock_device_repository.find = AsyncMock(
        return_value=Mock(id=uuid4(), token="valid_token", disabled=False)
    )
    mock_connect_log_repository.save = AsyncMock()

    # when
    response = await emqx_device_auth_service.authenticate(request_dto=emqx_authen_request_dto)

    # then
    assert response.result == "allow"
    assert response.is_superuser is False

    mock_connect_log_repository.save.assert_called_once()
