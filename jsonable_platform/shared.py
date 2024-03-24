from typing import Any, TypeVar, TypedDict
from json.encoder import JSONEncoder
# from hashlib import sha256

from .type import HashMethods, JSONSupportedBases, JSONAbleABCType

# from type import JSONSupportedTypes, JSONSupportedBases, JSONSupportedIterables

ENCODER = JSONEncoder()


def json_native_encode(obj: Any) -> str | None:
    """
    Get the result of native json encoded, if obj can't be converted to json, return None
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


def hash_class(cls: JSONAbleABCType | type[object]) -> tuple[str, HashMethods]:
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


def get_jsonable_keyname(obj: dict | tuple[JSONSupportedBases, dict]):
    keys = tuple(obj.keys()) if isinstance(obj, dict) else tuple(obj[1].keys())
    return keys[0] if len(keys) == 1 else None


def has_key(dic: dict, keyname: str):
    try:
        _ = dic[keyname]
        return True
    except KeyError:
        return False


def has_all_keys(dic: dict, typed: type[TypedDict], *, raise_error: bool = False) -> bool:
    if isinstance(getattr(typed, '__annotations__', None), dict):
        return all(
            has_key(dic, key) for key in typed.__annotations__.keys()
        )

    if raise_error:
        raise TypeError(f'Cannot get `__annotations__` from `{class_name(typed)}`')

    return True


def match_class_from_object(obj: Any, cls: JSONAbleABCType) -> bool:
    return isinstance(obj, cls)


def match_class_from_hash(hdx: str, cls: JSONAbleABCType) -> bool:
    return hdx == hash_class(cls)[0]
