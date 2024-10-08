from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.database.repository import Page
from app.database.repository.pagination import SortDirection
from app.module.device.exception.device_exception import DeviceNotFoundException
from app.module.device_data.model.connect_log import ConnectLog
from app.module.device_data.service.connect_log_service import ConnectLogService


@pytest.fixture
def mock_connect_log_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_device_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def connect_log_service(
    mock_connect_log_repository: AsyncMock,
    mock_device_repository: AsyncMock,
) -> ConnectLogService:
    return ConnectLogService(
        connect_log_repository=mock_connect_log_repository,
        device_repository=mock_device_repository,
    )


@pytest.fixture
def mock_connect_log() -> Mock:
    mock = Mock(spec=ConnectLog)
    mock.device_id = uuid4()
    mock.ts = datetime.now()
    mock.ip = "192.168.1.200"
    mock.connect_status = 0
    mock.keep_alive = 60
    return mock


async def test_get_connect_logs(
    connect_log_service: ConnectLogService,
    mock_connect_log_repository: AsyncMock,
    mock_connect_log: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = mock_connect_log.device_id
    page = 1
    page_size = 10
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 2)
    order_by: SortDirection = "asc"
    connect_log_page = Page(
        items=[mock_connect_log, mock_connect_log],
        page=1,
        page_size=10,
        total_items=2,
    )
    mock_connect_log_repository.find_all_with_paging.return_value = connect_log_page

    # when
    result = await connect_log_service.get_connect_logs(
        team_id=team_id,
        device_id=device_id,
        page=page,
        page_size=page_size,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by,
    )

    # then
    assert len(result.items) == 2
    assert result.page == 1
    assert result.page_size == 10
    assert result.total_items == 2


async def test_delete_connect_logs(
    connect_log_service: ConnectLogService,
    mock_connect_log_repository: AsyncMock,
    mock_connect_log: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = mock_connect_log.device_id
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 2)

    # when
    await connect_log_service.delete_connect_logs(
        team_id=team_id,
        device_id=device_id,
        start_date=start_date,
        end_date=end_date,
    )


async def test_validate_team_and_device(
    connect_log_service: ConnectLogService,
    mock_device_repository: AsyncMock,
    mock_connect_log: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = mock_connect_log.device_id
    mock_device_repository.exists_by_id_and_team_id.return_value = True

    # when
    await connect_log_service._validate_team_and_device(  # type: ignore
        team_id=team_id,
        device_id=device_id,
    )

    # then
    mock_device_repository.exists_by_id_and_team_id.assert_called_once_with(device_id, team_id)


async def test_validate_team_and_device_raise_device_not_found(
    connect_log_service: ConnectLogService,
    mock_device_repository: AsyncMock,
    mock_connect_log: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = mock_connect_log.device_id
    mock_device_repository.exists_by_id_and_team_id.return_value = False

    # when
    with pytest.raises(DeviceNotFoundException):
        await connect_log_service._validate_team_and_device(  # type: ignore
            team_id=team_id,
            device_id=device_id,
        )


async def test_validate_date_range(
    connect_log_service: ConnectLogService,
) -> None:
    # given
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 1, 2)

    # when
    connect_log_service._validate_date_range(  # type: ignore
        start_date=start_date,
        end_date=end_date,
    )


async def test_validate_date_range_raise_exception(
    connect_log_service: ConnectLogService,
) -> None:
    # given
    start_date = datetime(2021, 1, 2)
    end_date = datetime(2021, 1, 1)

    # when
    with pytest.raises(ValueError):
        connect_log_service._validate_date_range(  # type: ignore
            start_date=start_date,
            end_date=end_date,
        )
