from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead

from json import dumps as std_dumps, loads as std_loads, dump as std_dump, load as std_load
from json.decoder import JSONDecoder

from .type import JSONSupportedEditableIters, JSONSupportedTypes, EncoderFallbackType
from .type import DefinedClasses, JSONAbleABC, JSONAbleEncodedDict
from .shared import json_native_encode, class_name, hash_class, get_jsonable_keyname

JSONABLE_PREFIX = '$jsonable-'

_defined_classes: DefinedClasses = {
    'names': {},
    'classes': {}
}


def _search_jsonable_by_hash(hdx: str) -> type[JSONAbleABC] | None:
    cls = _defined_classes['classes'].get(hdx, None)
    if cls is not None:
        return cls

    cls = _defined_classes['names'].get(hdx, None)
    return cls  # None or class


def _search_jsonable_by_object(obj: JSONAbleABC) -> tuple[type[JSONAbleABC] | None, str | None]:
    hdx, hash_method = hash_class(type(obj))
    if hash_method == 'default':
        cls = _defined_classes['names'].get(hdx, None)
    else:
        cls = _defined_classes['classes'].get(hdx, None)

    return cls, hdx


def _register_jsonable(cls: type[JSONAbleABC], remove: bool = False):
    hdx, hash_method = hash_class(cls)

    if hash_method == 'default':
        if remove:
            _defined_classes['names'].pop(hdx, None)
        else:
            _defined_classes['names'][hdx] = cls
    else:
        if remove:
            _defined_classes['classes'].pop(hdx, None)
        else:
            _defined_classes['classes'][hdx] = cls


def register(cls: type[JSONAbleABC]):
    _register_jsonable(cls)


def unregister(cls: type[JSONAbleABC]):
    _register_jsonable(cls, remove=True)


def jsonable_encoder(obj: Any, fallback: EncoderFallbackType = None):
    if json_native_encode(obj):
        return obj

    cls, hdx = _search_jsonable_by_object(obj)
    if cls is not None and hdx is not None:
        data = cls.__jsonable_encode__(obj)
        if isinstance(data, JSONSupportedEditableIters):
            map(lambda _obj: jsonable_encoder(_obj, fallback), data)

        # { JSONABLE_PREFIX<class_name>: { 'data': data } }
        return {
            f'{JSONABLE_PREFIX}{class_name(obj)}': JSONAbleEncodedDict(hash=hdx, data=data)
        }

    res = fallback(obj) if fallback is not None else None
    if isinstance(res, JSONAbleEncodedDict):
        return {
            f'{JSONABLE_PREFIX}{class_name(obj)}': res
        }

    raise TypeError(f'Cannot convert {class_name(class_name(obj), "Unknown")} to JSON')


def dumps(obj: JSONSupportedTypes, fallback: EncoderFallbackType = None, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.pop('default', None)
    return std_dumps(obj, default=lambda _obj: jsonable_encoder(_obj, fallback), **kwargs)


class JSONAbleDecoder(JSONDecoder):
    def _convert2jsonable(self, iterable: JSONSupportedEditableIters):
        for key, value in iterable.copy().items() if isinstance(iterable, dict) else enumerate(iterable):
            if isinstance(value, dict):
                jsonable_key = get_jsonable_keyname(value)
                if isinstance(jsonable_key, str) and jsonable_key.startswith(JSONABLE_PREFIX):
                    jsonable_dict: JSONAbleEncodedDict = value[jsonable_key]

                    cls = _search_jsonable_by_hash(jsonable_dict['hash'])
                    if cls is None:
                        raise TypeError(
                            f'Cannot decode {jsonable_key[len(JSONABLE_PREFIX):] or "Unknown"} to Python Object'
                        )

                    if isinstance(jsonable_dict['data'], JSONSupportedEditableIters):
                        self._convert2jsonable(jsonable_dict['data'])

                    iterable[key] = cls.__jsonable_decode__(jsonable_dict['data'])
                    continue

            if isinstance(value, JSONSupportedEditableIters):
                self._convert2jsonable(value)

    def decode(self, s, _w=...):
        encoded_dict: dict = super().decode(s)

        self._convert2jsonable(encoded_dict)
        return encoded_dict


def loads(s: str, **kwargs):
    kwargs.pop('cls', None)

    return std_loads(s, cls=JSONAbleDecoder, **kwargs)


def dump(obj: Any, fp: 'SupportsWrite[str]', fallback: EncoderFallbackType = None, **kwargs):
    kwargs.pop('default', None)

    std_dump(obj, fp, default=lambda _obj: jsonable_encoder(_obj, fallback), **kwargs)


def load(fp: 'SupportsRead[str]', **kwargs):
    kwargs.pop('cls', None)

    return std_load(fp, cls=JSONAbleDecoder, **kwargs)


__all__ = (
    'dump', 'dumps', 'load', 'loads', 'register', 'unregister', 'jsonable_encoder', 'JSONAbleDecoder', 'JSONABLE_PREFIX'
)
