from dataclasses import dataclass, asdict, field
from typing_extensions import Self

from jsonable_platform import dumps, loads, JSONAbleABC, JSONSupportedTypes, register


@dataclass
class Person:
    name: str
    age: int = 0


@dataclass(kw_only=True)
class TestDataClass(JSONAbleABC):
    test_dict: dict = field(default_factory=lambda: {'a': Person(name='John')})

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        return asdict(obj)

    @classmethod
    def __jsonable_decode__(cls, data: JSONSupportedTypes) -> Self:
        return cls(**data)


register(TestDataClass)
print(asdict(TestDataClass()))

dumped = dumps({'test': TestDataClass()})
print(dumped)
print(loads(dumped))
