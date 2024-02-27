from .jsonable_datetime import datetime
from jsonable_platform import dumps, loads

from json import loads as parse

dic = {
    'now': datetime(2024, 1, 1),
    'delta': datetime(2024, 12, 31) - datetime(2024, 1, 1)
}

encoded = dumps(dic)

decoded = loads(encoded)


def test_encode_and_decode():
    assert decoded == dic, 'Decode failed'
