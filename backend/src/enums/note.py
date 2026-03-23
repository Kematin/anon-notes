from enum import Enum


class TimingForDestroy(str, Enum):
    """
    Время разрушения записки после прочтения
    """

    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
