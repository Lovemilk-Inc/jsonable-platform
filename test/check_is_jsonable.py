from jsonable_platform.shared import json_native_encode

EXPECTED_TRUE = ['1', '1.1', '"str"', 'true', 'null', '[1, 1.1, "str", true, null]', '[1, 1.1, "str", true, null]',
                 '{"1": true, "1.1": 1.1, "str": "str", "test": null}',
                 '[[1, 1.1, "str", true, null], [1, 1.1, "str", true, null]]']
EXPECTED_FALSE = [None for i in range(5)]


def func():
    pass


true = []
false = []

true.append(json_native_encode(1))
true.append(json_native_encode(1.1))
true.append(json_native_encode('str'))
true.append(json_native_encode(True))
true.append(json_native_encode(None))
true.append(json_native_encode([1, 1.1, 'str', True, None]))
true.append(json_native_encode((1, 1.1, 'str', True, None)))
true.append(json_native_encode(
    {
        1: 1,
        1.1: 1.1,
        'str': 'str',
        True: True,
        'test': None,  # do not use the `None` in dict keys!
    }
))

lst1 = [1, 1.1, 'str', True, None]
true.append(json_native_encode([lst1, lst1]))

false.append(json_native_encode(func))
false.append(json_native_encode([1, 1.1, 'str', True, None, func]))
false.append(json_native_encode((1, 1.1, 'str', True, None, func)))
false.append(json_native_encode(
    {
        1: 1,
        1.1: 1.1,
        'str': 'str',
        True: True,
        'test': None,  # do not use the `None` in dict keys!,
        'func': func
    }
))

lst2 = [1, 1.1, 'str', True, None, func]
false.append(json_native_encode([lst2, lst2]))


def test_convert():
    assert false == EXPECTED_FALSE, f'list `false`: {false} != {EXPECTED_FALSE}'
    assert true == EXPECTED_TRUE, f'list `true`: {true} != {EXPECTED_TRUE}'