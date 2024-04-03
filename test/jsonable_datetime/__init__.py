from jsonable_platform import JSONAbleABC, Self, register, JSONSupportedTypes
from datetime import datetime as std_datetime, timedelta as std_timedelta


class datetime(std_datetime, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return obj.timestamp()

    @classmethod
    def __jsonable_decode__(cls, data: JSONSupportedTypes) -> Self:
        return cls.fromtimestamp(data)


class timedelta(std_timedelta, JSONAbleABC):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return obj.total_seconds()

    @classmethod
    def __jsonable_decode__(cls, obj: JSONSupportedTypes) -> Self:
        return cls(seconds=obj)


register(datetime)
register(timedelta)
