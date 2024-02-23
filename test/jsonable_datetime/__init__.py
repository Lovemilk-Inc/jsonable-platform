from jsonable_platform import JSONAbleABC, Self, register, JSONAbleABCEncodedType
from datetime import datetime as std_datetime, timedelta as std_timedelta


class datetime(std_datetime, JSONAbleABC[float]):
    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return obj.timestamp()

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        return cls.fromtimestamp(data)


class timedelta(std_timedelta, JSONAbleABC[float]):
    @classmethod
    def __jsonable_encode__(cls, obj: Self):
        return obj.total_seconds()

    @classmethod
    def __jsonable_decode__(cls, obj) -> Self:
        return cls(seconds=obj)


register(datetime)
register(timedelta)
