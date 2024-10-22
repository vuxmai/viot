import json
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.database.repository import Page
from app.module.device.constants import DeviceType
from app.module.rule_action.constants import (
    MQTT_PRIVATE_TRIGGER_TOPIC,
    ActionType,
    EventType,
    RuleOperator,
)
from app.module.rule_action.dto.action_dto import (
    ActionCreateDto,
    ActionEmailConfigDto,
    ActionUpdateDto,
)
from app.module.rule_action.dto.rule_dto import Condition, RuleCreateDto, RuleUpdateDto
from app.module.rule_action.exception.rule_exception import RuleNotFoundException
from app.module.rule_action.service.rule_service import RuleService


@pytest.fixture
def mock_rule_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_emqx_rule_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_emqx_rule_builder_service() -> Mock:
    return Mock()


@pytest.fixture
def mock_device_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_team_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def rule_service(
    mock_rule_repository: AsyncMock,
    mock_emqx_rule_service: AsyncMock,
    mock_emqx_rule_builder_service: Mock,
    mock_device_service: AsyncMock,
    mock_team_service: AsyncMock,
) -> RuleService:
    return RuleService(
        rule_repository=mock_rule_repository,
        emqx_rule_service=mock_emqx_rule_service,
        emqx_rule_builder_service=mock_emqx_rule_builder_service,
        device_service=mock_device_service,
        team_service=mock_team_service,
    )


async def test_get_rule_by_id_and_team_id(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    mock_rule_repository.find_by_team_id_and_rule_id.return_value = mock_rule

    # when
    result = await rule_service.get_rule_by_id_and_team_id(team_id=team_id, rule_id=mock_rule.id)

    # then
    assert result.id == mock_rule.id
    assert result.name == mock_rule.name


async def test_get_rule_by_id_and_team_id_not_found(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
) -> None:
    # given
    team_id = uuid4()
    rule_id = uuid4()
    mock_rule_repository.find_by_team_id_and_rule_id.return_value = None

    # when
    with pytest.raises(RuleNotFoundException):
        await rule_service.get_rule_by_id_and_team_id(team_id=team_id, rule_id=rule_id)


async def test_get_paging_rules(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    mock_page = Page(
        items=[mock_rule, mock_rule],
        page=1,
        page_size=10,
        total_items=2,
    )
    mock_rule_repository.find_all_with_paging.return_value = mock_page

    # Act
    result = await rule_service.get_paging_rules(
        team_id=team_id,
        device_id=None,
        page=1,
        page_size=10,
    )

    # Assert
    assert result.page == 1
    assert result.page_size == 10
    assert result.total_items == 2
    assert len(result.items) == 2
    assert result.items[0].id == mock_rule.id
    assert result.items[0].name == mock_rule.name

    # Act
    result = await rule_service.get_paging_rules(
        team_id=team_id,
        device_id=uuid4(),
        page=1,
        page_size=10,
    )

    # Assert
    assert result.page == 1
    assert result.page_size == 10
    assert result.total_items == 2
    assert len(result.items) == 2
    assert result.items[0].id == mock_rule.id
    assert result.items[0].name == mock_rule.name


async def test_create_rule(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_emqx_rule_service: AsyncMock,
    mock_emqx_rule_builder_service: Mock,
    mock_device_service: AsyncMock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = uuid4()
    mock_device_service.get_device_by_id_and_team_id.return_value = Mock(type=DeviceType.DEVICE)
    mock_emqx_rule_builder_service.build_sql.return_value = "SELECT * FROM test"
    mock_rule_repository.save.return_value = mock_rule
    rule_create_dto = RuleCreateDto(
        name="Test Rule",
        description="Test Description",
        device_id=device_id,
        enable=True,
        event_type=EventType.DATA_EVENT,
        condition=Condition(field="temperature", operator=RuleOperator.gt, value=25),
        actions=[
            ActionCreateDto(
                name="Test Action",
                action_type=ActionType.EMAIL,
                config=ActionEmailConfigDto(email_address="test@example.com"),
            )
        ],
    )

    # when
    result = await rule_service.create_rule(team_id=team_id, rule_create_dto=rule_create_dto)

    # then
    assert result.id == mock_rule.id
    mock_rule_repository.save.assert_called_once()
    mock_emqx_rule_service.create_rule.assert_called_once()


async def test_update_rule(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_emqx_rule_service: AsyncMock,
    mock_emqx_rule_builder_service: Mock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = uuid4()
    rule_update_dto = RuleUpdateDto(
        name="Updated Rule",
        description="Updated Description",
        device_id=device_id,
        enable=True,
        event_type=EventType.DATA_EVENT,
        condition=Condition(field="temperature", operator=RuleOperator.gt, value=30),
        actions=[
            ActionUpdateDto(
                id=uuid4(),
                name="Test Action",
                action_type=ActionType.EMAIL,
                config=ActionEmailConfigDto(email_address="test@example.com"),
            )
        ],
    )
    mock_rule_repository.find_by_id_and_team_id.return_value = mock_rule
    mock_rule_repository.save.return_value = mock_rule
    mock_emqx_rule_builder_service.build_sql.return_value = "SELECT * FROM updated_test"

    # when
    result = await rule_service.update_rule(
        team_id=team_id, rule_id=mock_rule.id, rule_update_dto=rule_update_dto
    )

    # then
    assert result is not None
    mock_rule_repository.save.assert_called_once()
    mock_emqx_rule_service.update_rule.assert_called_once()


async def test_update_rule_existing_action(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_emqx_rule_service: AsyncMock,
    mock_emqx_rule_builder_service: Mock,
    mock_rule: Mock,
    mock_action: Mock,
) -> None:
    # Given
    team_id = uuid4()
    device_id = uuid4()
    rule_update_dto = RuleUpdateDto(
        name="Updated Rule",
        description="Updated Description",
        device_id=device_id,
        enable=True,
        event_type=EventType.DATA_EVENT,
        condition=Condition(field="temperature", operator=RuleOperator.gt, value=30),
        actions=[
            ActionUpdateDto(
                id=mock_action.id,
                name="Updated Action",
                action_type=ActionType.EMAIL,
                config=ActionEmailConfigDto(email_address="new@example.com"),
            )
        ],
    )

    mock_rule_repository.find_by_team_id_and_rule_id.return_value = mock_rule
    mock_rule_repository.save.return_value = mock_rule
    mock_emqx_rule_builder_service.build_sql.return_value = "SELECT * FROM updated_test"
    mock_emqx_rule_builder_service.get_mqtt_topic.return_value = "test/topic"

    # When
    result = await rule_service.update_rule(
        team_id=team_id, rule_id=mock_rule.id, rule_update_dto=rule_update_dto
    )

    # Then
    assert result is not None
    mock_rule_repository.save.assert_called_once()
    mock_emqx_rule_service.update_rule.assert_called_once()

    assert mock_action.name == "Updated Action"
    assert mock_action.config == ActionEmailConfigDto(email_address="new@example.com").model_dump()


async def test_update_rule_raise_rule_not_found(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    device_id = uuid4()
    rule_update_dto = RuleUpdateDto(
        name="Updated Rule",
        description="Updated Description",
        device_id=device_id,
        enable=True,
        event_type=EventType.DATA_EVENT,
        condition=Condition(field="temperature", operator=RuleOperator.gt, value=30),
        actions=[
            ActionUpdateDto(
                id=uuid4(),
                name="Test Action",
                action_type=ActionType.EMAIL,
                config=ActionEmailConfigDto(email_address="test@example.com"),
            )
        ],
    )
    mock_rule_repository.find_by_team_id_and_rule_id.return_value = None

    # when
    with pytest.raises(RuleNotFoundException):
        await rule_service.update_rule(
            team_id=team_id, rule_id=mock_rule.id, rule_update_dto=rule_update_dto
        )


def test__create_emqx_action_dto(rule_service: RuleService, mock_rule: Mock) -> None:
    # Given
    mock_rule.device_id = 1
    mock_rule.id = 123
    mock_rule.actions = [Mock(id=10), Mock(id=20)]  # Mock action objects with ids

    # When
    result = rule_service._create_emqx_action_dto(mock_rule)  # type: ignore

    # Then
    assert result is not None
    assert result.function == "republish"

    args = result.args
    assert args.topic == MQTT_PRIVATE_TRIGGER_TOPIC
    assert args.qos == 2
    assert args.retain is True
    assert args.direct_dispatch is True

    # Check payload
    payload_json = args.payload
    assert payload_json is not None

    # Parse the payload JSON to dictionary for further validation
    payload_dict = json.loads(payload_json)

    assert payload_dict["device_id"] == str(mock_rule.device_id)
    assert payload_dict["rule_id"] == str(mock_rule.id)
    assert payload_dict["action_ids"] == [str(action.id) for action in mock_rule.actions]
    assert payload_dict["payload"] == "${payload}"
    assert payload_dict["ts"] == "${ts}"


async def test_delete_rule(
    rule_service: RuleService,
    mock_rule_repository: AsyncMock,
    mock_emqx_rule_service: AsyncMock,
    mock_rule: Mock,
) -> None:
    # given
    team_id = uuid4()
    rule_id = uuid4()
    mock_rule_repository.delete_by_team_id_and_rule_id.return_value = None

    # when
    await rule_service.delete_rule(team_id=team_id, rule_id=rule_id)

    # then
    mock_rule_repository.delete_by_team_id_and_rule_id.assert_called_once()
    mock_emqx_rule_service.delete_rule.assert_called_once()
