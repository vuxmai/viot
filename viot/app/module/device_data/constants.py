from enum import IntEnum, StrEnum


class ConnectStatus(IntEnum):
    """Connect status

    DISCONNECTED = 0
    CONNECTED = 1
    """

    DISCONNECTED = 0
    CONNECTED = 1


class AggregationType(StrEnum):
    """Aggregation type

    AVG = avg
    SUM = sum
    MIN = min
    MAX = max
    COUNT = count
    """

    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"


class IntervalType(StrEnum):
    """Interval type

    SECOND = second
    MINUTE = minute
    HOUR = hour
    DAY = day
    WEEK = week
    MONTH = month
    YEAR = year
    """

    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
