from typing import Any, TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead

from json import dumps as std_dumps, loads as std_loads, dump as std_dump, load as std_load

from .type import JSONSupportedEditableIters, JSONSupportedTypes, JSONSupportedBases, JSONAbleABCType, RequirementsType
from .type import EncoderFallbackType, DecoderFallbackType, JSONAbleEncodedDict, RequiredEncodedDict
from .type import DefinedClasses, DefinedClassesData, JSONAbleABC, JSONAbleEncodedType
from .shared import json_native_encode, class_name, hash_class, get_jsonable_keyname, has_all_keys
from .shared import match_class_from_object, match_class_from_hash

JSONABLE_PREFIX = '$jsonable'
REPR_CLASSNAME: bool = False

_defined_classes: DefinedClasses = {
    'names': {},
    'classes': {}
}


def _search_jsonable_by_hash(hdx: str) -> tuple[JSONAbleABCType, RequirementsType] | None:
    data = _defined_classes['classes'].get(hdx, None)
    if data is not None:
        return data['cls'], data['requirements']

    data = _defined_classes['names'].get(hdx, None)
    if data is not None:
        return data['cls'], data['requirements']


def _search_jsonable_by_object(obj: JSONAbleABC) -> tuple[tuple[JSONAbleABCType, RequirementsType] | None, str | None]:
    hdx, hash_method = hash_class(type(obj))
    if hash_method == 'default':
        data = _defined_classes['names'].get(hdx, None)
    else:
        data = _defined_classes['classes'].get(hdx, None)

    if data is None:
        return None, None

    return (data['cls'], data['requirements']), hdx


def _register_jsonable(cls: JSONAbleABCType, *requirements: JSONAbleABCType, remove: bool = False):
    hdx, hash_method = hash_class(cls)

    if hash_method == 'default':
        if remove:
            _defined_classes['names'].pop(hdx, None)
        else:
            _defined_classes['names'][hdx] = DefinedClassesData(cls=cls, requirements=requirements)
    else:
        if remove:
            _defined_classes['classes'].pop(hdx, None)
        else:
            _defined_classes['classes'][hdx] = DefinedClassesData(cls=cls, requirements=requirements)


def register(cls: JSONAbleABCType, *requirements: JSONAbleABCType):
    _register_jsonable(cls, *requirements)


def unregister(cls: JSONAbleABCType):
    _register_jsonable(cls, remove=True)


def jsonable_encoder(
        obj: JSONSupportedTypes | JSONAbleABC, fallback: EncoderFallbackType = None,
) -> JSONSupportedBases | dict[str, JSONAbleEncodedType]:
    if json_native_encode(obj):
        return obj

    try:
        return directly_encoder(obj)
    except ValueError:
        res = fallback(obj) if fallback is not None else None
        if isinstance(res, dict) and has_all_keys(res, JSONAbleEncodedType):
            return {
                f'{JSONABLE_PREFIX}-{class_name(obj) if not REPR_CLASSNAME else repr(obj)}': res
            }

        raise


def dumps(obj: JSONSupportedTypes, fallback: EncoderFallbackType = None, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.pop('default', None)

    return std_dumps(obj, default=lambda _obj: jsonable_encoder(_obj, fallback), **kwargs)


def jsonable_decoder(
        object_pairs: Iterable[tuple[JSONSupportedBases, JSONSupportedBases]],
        fallback: DecoderFallbackType = None,
) -> dict[JSONSupportedBases, JSONSupportedBases | JSONAbleABC]:
    result = {}

    for key, value in object_pairs:
        if not isinstance(value, JSONSupportedEditableIters):
            result[key] = value

        if isinstance(value, list):
            result[key] = list(jsonable_decoder(enumerate(value), fallback).values())
            continue

        if not isinstance(value, dict):
            result[key] = value
            continue

        jsonable_key = get_jsonable_keyname(value)
        if not (isinstance(jsonable_key, str) and jsonable_key.startswith(JSONABLE_PREFIX + '-')):
            result[key] = jsonable_decoder(value.items(), fallback)
            continue

        jsonable_dict: JSONAbleEncodedType = value[jsonable_key]
        try:
            res = directly_decoder(jsonable_dict)
            result[key] = res if res is not None else value
            continue
        except KeyError:
            result[key] = value
            continue
        except ValueError:
            if fallback is None:
                raise ValueError(
                    f'Cannot decode {jsonable_key[len(JSONABLE_PREFIX) + 1:] or "Unknown"} to Python Object'
                )

            result[key] = fallback(jsonable_dict)
            continue

    return result


def loads(s: str, fallback: DecoderFallbackType = None, **kwargs):
    # kwargs.pop('cls', None)
    kwargs.pop('object_pairs_hook', None)

    # return std_loads(s, cls=JSONAbleDecoder, **kwargs)
    return std_loads(s, object_pairs_hook=lambda _pairs: jsonable_decoder(_pairs, fallback), **kwargs)


def dump(obj: Any, fp: 'SupportsWrite[str]', fallback: EncoderFallbackType = None, **kwargs):
    kwargs.pop('default', None)

    std_dump(obj, fp, default=lambda _obj: jsonable_encoder(_obj, fallback), **kwargs)


def load(fp: 'SupportsRead[str]', fallback: DecoderFallbackType = None, **kwargs):
    # kwargs.pop('cls', None)
    kwargs.pop('object_pairs_hook', None)

    # return std_load(fp, cls=JSONAbleDecoder, **kwargs)
    return std_load(fp, object_pairs_hook=lambda _pairs: jsonable_decoder(_pairs, fallback), **kwargs)


def directly_encoder(obj: JSONAbleABC):
    requirements = ()
    parent = getattr(obj, '__jsonable_parent__', '')
    if parent:
        parend_searched = _search_jsonable_by_hash(parent)
        if parend_searched is not None:
            requirements = parend_searched[1]

    for requirement in requirements:
        if not match_class_from_object(obj, requirement):
            continue

        data = requirement.__jsonable_encode__(obj)
        return {
            f'{JSONABLE_PREFIX}-{class_name(obj) if not REPR_CLASSNAME else repr(obj)}': RequiredEncodedDict(
                hash=hash_class(requirement)[0], data=data, parent=parent
            )
        }

    search_result, hdx = _search_jsonable_by_object(obj)
    if search_result is not None and hdx is not None:
        cls, defined_requirements = search_result

        data = cls.__jsonable_encode__(obj)
        if defined_requirements:
            def _each(_iter: list | dict):
                """
                each every JSONAbleABC object in anywhere in parent object to set the parent hash
                :param _iter: list or dict
                :return: None
                """
                for _item in _iter.values() if isinstance(_iter, dict) else _iter:
                    if isinstance(_item, (list, dict)):
                        _each(_item)
                    elif isinstance(_item, JSONAbleABC):
                        setattr(_item, '__jsonable_parent__', hdx)
                        _each(vars(_item))

            if isinstance(data, (list, dict)):
                _each(data)

        # { <JSONABLE_PREFIX><class_name>: { 'hash': hash, 'data': data } }
        return {
            f'{JSONABLE_PREFIX}-{class_name(obj) if not REPR_CLASSNAME else repr(obj)}':
                JSONAbleEncodedDict(
                    hash=hdx, data=data
                )
        }

    raise ValueError(f'Cannot convert {class_name(obj, "Unknown")} to JSON')


def directly_decoder(
        encoded: JSONAbleEncodedType,
) -> JSONAbleABC:
    if not has_all_keys(encoded, JSONAbleEncodedType):
        raise KeyError('Miss key(s)')

    requirements = ()
    parent = encoded.get('parent', '')
    if parent:
        parend_searched = _search_jsonable_by_hash(parent)
        if parend_searched is not None:
            requirements = parend_searched[1]

    for requirement in requirements:
        if not match_class_from_hash(encoded['hash'], requirement):
            continue

        return requirement.__jsonable_decode__(encoded['data'])

    search_result = _search_jsonable_by_hash(encoded['hash'])

    if search_result is not None:
        cls, defined_requirements = search_result

        data = encoded['data']
        return cls.__jsonable_decode__(data)

    raise ValueError(f'Cannot decode to Python Object')


__all__ = (
    'dump', 'dumps', 'load', 'loads', 'register', 'unregister', 'jsonable_encoder',
    'jsonable_decoder', 'directly_decoder', 'directly_encoder',
    'JSONABLE_PREFIX', 'REPR_CLASSNAME'
)
