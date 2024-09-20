from enum import IntEnum


class DeviceType(IntEnum):
    """Device type

    DEVICE = 0
    GATEWAY = 1
    SUB_DEVICE = 2
    """

    DEVICE = 0
    GATEWAY = 1
    SUB_DEVICE = 2


class DeviceStatus(IntEnum):
    """Device status

    OFFLINE = 0
    ONLINE = 1
    """

    OFFLINE = 0
    ONLINE = 1


class UplinkProtocol(IntEnum):
    """Protocol for uplink data from sub device to gateway.

    MQTT = 0
    MODBUS = 1
    ZIGBEE = 2
    """

    MQTT = 0
    MODBUS = 1
    ZIGBEE = 2
