from .jsonable_datetime import datetime
from jsonable_platform import dumps, loads

from json import loads as parse

dic = {
    'now': datetime(2024, 1, 1),
    'delta': datetime(2024, 12, 31) - datetime(2024, 1, 1)
}

encoded = dumps(dic)
print(encoded)

decoded = loads(encoded)
print(decoded)
print(decoded['delta'].total_seconds())


def test_encode():
    assert parse(encoded.replace(' ', '')) == parse(
        '{"now": {"$jsonable-datetime": {"hash": "datetime", "data": 1704038400.0}}, '
        '"delta": {"$jsonable-timedelta": {"hash": "timedelta", "data": 31536000.0}}}'
    ), 'Encode failed'


def test_decode():
    assert decoded == dic, 'Decode failed'
