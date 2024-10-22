from enum import IntEnum, StrEnum

# MQTT topics
MQTT_DEVICE_DATA_TOPIC = "v2/devices/me/data"
MQTT_DEVICE_ATTRIBUTES_TOPIC = "v2/devices/me/attributes"
MQTT_SUB_DEVICE_DATA_TOPIC = "v2/devices/sub/data"
MQTT_SUB_DEVICE_ATTRIBUTES_TOPIC = "v2/devices/sub/attributes"
MQTT_CONNECTED_EVENT_TOPIC = "$events/client_connected"
MQTT_DISCONNECTED_EVENT_TOPIC = "$events/client_disconnected"
MQTT_PRIVATE_TRIGGER_TOPIC = "v2/private/trigger"

# EMQX where device key
SUB_DEVICE_KEY = "sub_device_id"


class EventType(IntEnum):
    """
    Enum class for event type
    """

    DATA_EVENT = 0
    # ATTRIBUTES_EVENT = 1
    # RPC_EVENT = 2
    CONNECTED_EVENT = 3
    DISCONNECTED_EVENT = 4


class RuleOperator(StrEnum):
    """
    Enum class for rule operator
    """

    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="
    eq = "="
    neq = "!="


class RuleLogic(StrEnum):
    """
    Enum class for rule logic
    """

    AND = "AND"
    OR = "OR"


class ActionType(IntEnum):
    """
    Enum class for action type
    """

    # ALARM = 0
    EMAIL = 1
    # WEBHOOK = 2
