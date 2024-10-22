from uuid import UUID

from ..constants import (
    MQTT_CONNECTED_EVENT_TOPIC,
    MQTT_DEVICE_DATA_TOPIC,
    MQTT_DISCONNECTED_EVENT_TOPIC,
    MQTT_SUB_DEVICE_DATA_TOPIC,
    SUB_DEVICE_KEY,
    EventType,
    RuleOperator,
)
from ..dto.rule_dto import Condition, ConditionLogic

MQTT_TOPIC_MAP: dict[EventType, str] = {
    EventType.CONNECTED_EVENT: MQTT_CONNECTED_EVENT_TOPIC,
    EventType.DISCONNECTED_EVENT: MQTT_DISCONNECTED_EVENT_TOPIC,
    EventType.DATA_EVENT: MQTT_DEVICE_DATA_TOPIC,
}


class EmqxRuleBuilderService:
    def build_sql(
        self,
        device_id: UUID,
        is_sub_device: bool,
        topic: str,
        condition: ConditionLogic | Condition,
    ) -> str:
        """
        Build an SQL query that can be used in an EMQX rule engine.

        Args:
            device_id (UUID): The ID of the device to build the query for.
            is_sub_device (bool): Whether the device is a sub-device.
            event_type (EventType): The type of event to build the query for.
            condition (ConditionLogic | Condition): The condition to build the query for.

        Returns:
            str: The built EMQX SQL query.
        """
        sql_condition = self._convert_condition_schema_to_sql(condition)
        device_id_field = SUB_DEVICE_KEY if is_sub_device else "clientid"

        return (
            f"SELECT {device_id_field} AS device_id, payload,\n"
            f"now_rfc3339('millisecond') AS ts\n"
            f"FROM '{topic}'\n"
            f"WHERE device_id = '{str(device_id)}'\n"
            f"AND {sql_condition}"
        )

    def get_mqtt_topic(self, event_type: EventType, is_sub_device: bool) -> str:
        """
        Build an MQTT topic based on the event type and whether the device is a sub-device.

        Args:
            event_type (EventType): The type of event to build the topic for.
            is_sub_device (bool): Whether the device is a sub-device.

        Returns:
            str: The built MQTT topic.
        """

        topic = MQTT_TOPIC_MAP[event_type]
        return MQTT_SUB_DEVICE_DATA_TOPIC if is_sub_device else topic

    def _convert_condition_schema_to_sql(self, condition: ConditionLogic | Condition) -> str:
        """
        Convert a Condition or ConditionLogic object to a string that can be used in
        an EMQX rule condition.

        Args:
            condition (ConditionLogic | Condition): The condition to convert.

        Returns:
            str: SQL-compatible condition string.
        """
        if isinstance(condition, Condition):
            value = self._format_condition_value(condition)
            return f"payload.{condition.field} {condition.operator} {value}"

        logic = condition.logic
        sub_conditions = condition.conditions
        if len(sub_conditions) < 2:
            raise ValueError("Condition logic must contain at least two sub-conditions.")

        sql_conditions = [
            self._convert_condition_schema_to_sql(sub_condition) for sub_condition in sub_conditions
        ]
        return f"({f' {logic} '.join(sql_conditions)})"

    def _format_condition_value(self, condition: Condition) -> str | int | bool:
        """
        Format and validate the value of a condition based on its operator.

        Args:
            condition (Condition): The condition to format.

        Returns:
            str | int | bool: The formatted condition value for SQL.

        Raises:
            ValueError: If the operator is not allowed for the type of value.
        """
        if isinstance(condition.value, str):
            if condition.operator not in (RuleOperator.eq, RuleOperator.neq):
                raise ValueError(
                    f"Operator '{condition.operator}' is not allowed "
                    f"for string values in field '{condition.field}'"
                )
            return f"'{condition.value}'"

        if isinstance(condition.value, bool):
            # Convert True/False to 'true'/'false' for SQL
            return str(condition.value).lower()

        return condition.value
