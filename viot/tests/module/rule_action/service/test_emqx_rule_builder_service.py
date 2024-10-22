from uuid import uuid4

import pytest

from app.module.rule_action.constants import (
    MQTT_DEVICE_DATA_TOPIC,
    MQTT_SUB_DEVICE_DATA_TOPIC,
    EventType,
    RuleLogic,
    RuleOperator,
)
from app.module.rule_action.dto.rule_dto import Condition, ConditionLogic
from app.module.rule_action.service.emqx_rule_builder_service import EmqxRuleBuilderService


@pytest.fixture
def emqx_sql_builder_service() -> EmqxRuleBuilderService:
    return EmqxRuleBuilderService()


def test_build_sql_with_single_condition(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    device_id = uuid4()
    condition = Condition(field="temperature", operator=RuleOperator.gt, value=25)
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=False,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT clientid AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND payload.temperature > 25"
    )

    assert sql == expected_sql


def test_build_sql_with_condition_logic(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    device_id = uuid4()
    condition = ConditionLogic(
        logic=RuleLogic.AND,
        conditions=[
            Condition(field="temperature", operator=RuleOperator.gt, value=25),
            Condition(field="humidity", operator=RuleOperator.lt, value=60),
        ],
    )
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=True,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT sub_device_id AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND (payload.temperature > 25 AND payload.humidity < 60)"
    )

    assert sql == expected_sql


def test_build_sql_with_string_condition(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    device_id = uuid4()
    condition = Condition(field="status", operator=RuleOperator.eq, value="active")
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=False,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT clientid AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND payload.status = 'active'"
    )

    assert sql == expected_sql


def test_build_sql_with_boolean_condition(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    device_id = uuid4()
    condition = Condition(field="is_active", operator=RuleOperator.eq, value=True)
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=False,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT clientid AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND payload.is_active = true"
    )

    assert sql == expected_sql


def test_build_sql_with_invalid_string_operator(
    emqx_sql_builder_service: EmqxRuleBuilderService,
) -> None:
    # given
    device_id = uuid4()
    condition = Condition(field="status", operator=RuleOperator.gt, value="active")
    topic = "test/topic"

    # when
    with pytest.raises(
        ValueError,
        match=f"Operator '{RuleOperator.gt}' is not allowed for string values in field 'status'",
    ):
        emqx_sql_builder_service.build_sql(
            device_id=device_id,
            is_sub_device=False,
            topic=topic,
            condition=condition,
        )


def test_build_sql_with_nested_condition_logic(
    emqx_sql_builder_service: EmqxRuleBuilderService,
) -> None:
    # given
    device_id = uuid4()
    condition = ConditionLogic(
        logic=RuleLogic.OR,
        conditions=[
            ConditionLogic(
                logic=RuleLogic.AND,
                conditions=[
                    Condition(field="temperature", operator=RuleOperator.gt, value=25),
                    Condition(field="humidity", operator=RuleOperator.lt, value=60),
                ],
            ),
            Condition(field="status", operator=RuleOperator.eq, value="critical"),
        ],
    )
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=False,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT clientid AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND ((payload.temperature > 25 AND payload.humidity < 60) OR payload.status = 'critical')"
    )

    assert sql == expected_sql


def test_build_sql_with_nested_condition_logic_and_sub_device(
    emqx_sql_builder_service: EmqxRuleBuilderService,
) -> None:
    # given
    device_id = uuid4()
    condition = ConditionLogic(
        logic=RuleLogic.OR,
        conditions=[
            ConditionLogic(
                logic=RuleLogic.AND,
                conditions=[
                    Condition(field="temperature", operator=RuleOperator.gt, value=25),
                    Condition(field="humidity", operator=RuleOperator.lt, value=60),
                ],
            ),
            Condition(field="status", operator=RuleOperator.eq, value="critical"),
        ],
    )
    topic = "test/topic"

    # when
    sql = emqx_sql_builder_service.build_sql(
        device_id=device_id,
        is_sub_device=True,
        topic=topic,
        condition=condition,
    )

    # then
    expected_sql = (
        "SELECT sub_device_id AS device_id, payload,\n"
        "now_rfc3339('millisecond') AS ts\n"
        f"FROM '{topic}'\n"
        f"WHERE device_id = '{str(device_id)}'\n"
        "AND ((payload.temperature > 25 AND payload.humidity < 60) OR payload.status = 'critical')"
    )

    assert sql == expected_sql


def test_build_sql_with_nested_condition_logic_with_single_sub_condition(
    emqx_sql_builder_service: EmqxRuleBuilderService,
) -> None:
    # given
    device_id = uuid4()
    condition = ConditionLogic(
        logic=RuleLogic.AND,
        conditions=[Condition(field="temperature", operator=RuleOperator.gt, value=25)],
    )
    topic = "test/topic"

    # when
    with pytest.raises(
        ValueError, match="Condition logic must contain at least two sub-conditions."
    ):
        emqx_sql_builder_service.build_sql(
            device_id=device_id,
            is_sub_device=False,
            topic=topic,
            condition=condition,
        )


def test_get_mqtt_topic(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    event_type = EventType.DATA_EVENT
    is_sub_device = False

    # when
    topic = emqx_sql_builder_service.get_mqtt_topic(event_type, is_sub_device)

    # then
    assert topic == MQTT_DEVICE_DATA_TOPIC


def test_get_mqtt_topic_with_sub_device(emqx_sql_builder_service: EmqxRuleBuilderService) -> None:
    # given
    event_type = EventType.DATA_EVENT
    is_sub_device = True

    # when
    topic = emqx_sql_builder_service.get_mqtt_topic(event_type, is_sub_device)

    # then
    assert topic == MQTT_SUB_DEVICE_DATA_TOPIC
