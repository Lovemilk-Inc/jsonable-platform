from unittest import TestCase
from typing import Union

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
    def __init__(self, recursion_test: Union['RecursionTest', None] = None):
        self.recursion_test = recursion_test

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        return {'recursion_test': obj.recursion_test}

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        return cls(data['recursion_test'])

    def __eq__(self, other):
        return hasattr(other, 'recursion_test') and self.recursion_test == other.recursion_test


def test_recursion():
    register(RecursionTest)

    test = RecursionTest(RecursionTest(RecursionTest(None)))

    encoded = dumps({'test': test})

    decoded = loads(encoded)

    assert decoded['test'] == test, 'recursion test failed'
