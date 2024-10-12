from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.database.repository.pagination import Page
from app.module.device.constants import DeviceType
from app.module.device.dto.device_dto import DeviceCreateDto
from app.module.device.exception.device_exception import DeviceNotFoundException
from app.module.device.service.device_service import DeviceService
from app.module.team.exception.team_exception import TeamNotFoundException


@pytest.fixture
def mock_device_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_team_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def device_service(
    mock_device_repository: AsyncMock,
    mock_team_repository: AsyncMock,
) -> DeviceService:
    return DeviceService(
        device_repository=mock_device_repository,
        team_repository=mock_team_repository,
    )


async def test_get_device_by_id_and_team_id(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
    mock_device: Mock,
) -> None:
    # given
    device_id = uuid4()
    team_id = uuid4()
    mock_device_repository.find_by_device_id_and_team_id.return_value = mock_device

    # when
    result = await device_service.get_device_by_id_and_team_id(device_id=device_id, team_id=team_id)

    # then
    assert result.id == mock_device.id
    assert result.name == mock_device.name
    assert result.description == mock_device.description
    assert result.device_type == mock_device.device_type
    assert result.token == mock_device.token
    assert result.status == mock_device.status
    assert result.image_url == mock_device.image_url
    assert result.disabled == mock_device.disabled
    assert result.last_connection == mock_device.last_connection
    assert result.meta_data == mock_device.meta_data


async def test_get_device_by_id_and_team_id_raise_device_not_found(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    team_id = uuid4()
    mock_device_repository.find_by_device_id_and_team_id.return_value = None

    # when
    with pytest.raises(DeviceNotFoundException):
        await device_service.get_device_by_id_and_team_id(device_id=device_id, team_id=team_id)


async def test_get_all_devices_belong_to_team(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
    mock_device: Mock,
) -> None:
    # given
    team_id = uuid4()
    page = 1
    page_size = 10
    device_type = DeviceType.DEVICE
    mock_device_repository.find_all_with_paging.return_value = Page(
        items=[mock_device, mock_device], total_items=2, page=0, page_size=20
    )

    # when
    result = await device_service.get_all_devices_belong_to_team(
        team_id=team_id, page=page, page_size=page_size, device_type=device_type
    )

    # then
    assert len(result.items) == 2
    assert result.total_items == 2
    assert result.page == 0
    assert result.page_size == 20
    assert result.items[0].id == mock_device.id
    assert result.items[0].name == mock_device.name
    assert result.items[0].description == mock_device.description
    assert result.items[0].device_type == mock_device.device_type
    assert result.items[0].token == mock_device.token
    assert result.items[0].status == mock_device.status
    assert result.items[0].image_url == mock_device.image_url
    assert result.items[0].disabled == mock_device.disabled
    assert result.items[0].last_connection == mock_device.last_connection
    assert result.items[0].meta_data == mock_device.meta_data


async def test_create_device(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
    mock_team_repository: AsyncMock,
    mock_device: Mock,
) -> None:
    # given
    team_id = uuid4()
    dto = DeviceCreateDto(
        name="device",
        description="description",
        device_type=DeviceType.DEVICE,
    )
    mock_team_repository.exists_by_id.return_value = True
    mock_device_repository.save.return_value = mock_device

    # when
    result = await device_service.create_device(team_id=team_id, device_create_dto=dto)

    # then
    assert result.id == mock_device.id
    assert result.name == mock_device.name
    assert result.description == mock_device.description
    assert result.device_type == mock_device.device_type
    assert result.token == mock_device.token
    assert result.status == mock_device.status
    assert result.image_url == mock_device.image_url
    assert result.disabled == mock_device.disabled
    assert result.last_connection == mock_device.last_connection
    assert result.meta_data == mock_device.meta_data


async def test_create_device_raise_team_not_found(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
    mock_team_repository: AsyncMock,
) -> None:
    # given
    team_id = uuid4()
    dto = DeviceCreateDto(
        name="device",
        description="description",
        device_type=DeviceType.DEVICE,
    )
    mock_team_repository.exists_by_id.return_value = False

    # when
    with pytest.raises(TeamNotFoundException):
        await device_service.create_device(team_id=team_id, device_create_dto=dto)


async def test_delete_device_by_id_and_team_id(
    device_service: DeviceService,
    mock_device_repository: AsyncMock,
) -> None:
    # given
    device_id = uuid4()
    team_id = uuid4()

    # when
    await device_service.delete_device_by_id_and_team_id(device_id=device_id, team_id=team_id)

    # then
    mock_device_repository.delete_by_device_id_and_team_id.assert_called_once_with(
        device_id, team_id
    )
