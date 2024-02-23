from unittest import TestCase
from .jsonable_datetime import datetime
from jsonable_platform import (
    dumps,
    register,
    JSONAbleABC,
    JSONAbleABCEncodedType,
    Self,
    loads
)


class Test(JSONAbleABC):
    def __init__(self, content: str):
        self.content = content

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return {'content': obj.content}

    @classmethod
    def __jsonable_decode__(cls, obj: JSONAbleABCEncodedType) -> Self:
        return cls(obj['content'])

    def __eq__(self, other):
        return hasattr(other, 'content') and self.content == self.content


class ConvertTest(TestCase):
    def test_convert(self):
        register(Test)

        test = Test(content='test string')

        encoded = dumps({'test': test, 'test2': {'test3': test, 'test4': [test]}}, ensure_ascii=False)

        self.assertEqual({'test': test, 'test2': {'test3': test, 'test4': [test]}}, loads(encoded))


class RecursionTest(JSONAbleABC):
    def __init__(self, _datetime: datetime):
        self.datetime = _datetime

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return {'datetime': obj.datetime}

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        return cls(data['datetime'])

    def __eq__(self, other):
        return hasattr(other, 'datetime') and self.datetime == other.datetime


def test_recursion():
    register(RecursionTest)

    test = RecursionTest(datetime(2024, 1, 1))

    encoded = dumps({'test': test})

    decoded = loads(encoded)

    assert decoded['test'] == test and isinstance(decoded['test'].datetime, datetime), 'recursion test failed'
