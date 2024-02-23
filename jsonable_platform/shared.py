from typing import Any, TypeVar
from json.encoder import JSONEncoder
from hashlib import sha256

from .type import HashMethods, JSONSupportedBases

# from type import JSONSupportedTypes, JSONSupportedBases, JSONSupportedIterables

ENCODER = JSONEncoder()


def json_native_encode(obj: Any) -> str | None:
    """
    Get the result of native json encoded, if obj can't be converted to json, return empty (...)
    :param obj: Object you want to check
    :return: str -> native jsonable; None -> not native jsonable;
    """

    try:
        return ENCODER.encode(obj)
    except TypeError:
        return


DefaultType = TypeVar('DefaultType')


def class_name(obj_or_cls: Any, default: DefaultType = None) -> str | DefaultType:
    if hasattr(obj_or_cls, '__name__'):
        return obj_or_cls.__name__

    obj_or_cls = type(obj_or_cls)
    if hasattr(obj_or_cls, '__name__'):
        return obj_or_cls.__name__

    return default


def hash_class(cls: Any) -> tuple[str, HashMethods]:
    res = None
    func = getattr(cls, '__jsonable_hash__', None)
    if callable(func):
        res = func()

    cls_name = class_name(cls)
    if cls_name is None:
        raise ValueError(f'{cls}\'s name is not defined')

    if isinstance(res, str):
        return res, 'custom'
    else:
        # return sha256(cls_name.encode()).hexdigest(), 'default'
        return cls_name, 'default'


def get_jsonable_keyname(obj: dict):
    keys = tuple(obj.keys())
    return keys[0] if len(keys) == 1 else None
