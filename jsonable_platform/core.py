from typing import Any, TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead

from deprecated import deprecated
from json import dumps as std_dumps, loads as std_loads, dump as std_dump, load as std_load
from json.decoder import JSONDecoder

from .type import JSONSupportedEditableIters, JSONSupportedTypes, JSONSupportedBases
from .type import EncoderFallbackType, DecoderFallbackType
from .type import DefinedClasses, JSONAbleABC, JSONAbleEncodedDict
from .shared import json_native_encode, class_name, hash_class, get_jsonable_keyname, has_all_keys

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


def jsonable_encoder(
        obj: JSONSupportedTypes | JSONAbleABC, fallback: EncoderFallbackType = None
) -> JSONSupportedBases | dict[str, JSONAbleEncodedDict]:
    if json_native_encode(obj):
        return obj

    try:
        return directly_encoder(obj)
    except ValueError:
        res = fallback(obj) if fallback is not None else None
        if isinstance(res, JSONAbleEncodedDict):
            return {
                f'{JSONABLE_PREFIX}{class_name(obj)}': res
            }

        raise


def dumps(obj: JSONSupportedTypes, fallback: EncoderFallbackType = None, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.pop('default', None)

    return std_dumps(obj, default=lambda _obj: jsonable_encoder(_obj, fallback), **kwargs)


@deprecated(version='0.0.2', reason='use object_pairs_hook argument instead')
class JSONAbleDecoder(JSONDecoder):
    def _convert2jsonable(self, iterable: JSONSupportedEditableIters):
        for key, value in iterable.copy().items() if isinstance(iterable, dict) else enumerate(iterable):
            if isinstance(value, dict):
                jsonable_key = get_jsonable_keyname(value)
                if isinstance(jsonable_key, str) and jsonable_key.startswith(JSONABLE_PREFIX):
                    jsonable_dict: JSONAbleEncodedDict = value[jsonable_key]

                    if has_all_keys(jsonable_dict, JSONAbleEncodedDict):
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
        if not (isinstance(jsonable_key, str) and jsonable_key.startswith(JSONABLE_PREFIX)):
            result[key] = jsonable_decoder(value.items(), fallback)
            continue

        jsonable_dict: JSONAbleEncodedDict = value[jsonable_key]
        try:
            result[key] = directly_decoder(jsonable_dict)
            continue
        except KeyError:
            result[key] = value
            continue
        except ValueError:
            if fallback is None:
                raise ValueError(
                    f'Cannot decode {jsonable_key[len(JSONABLE_PREFIX):] or "Unknown"} to Python Object'
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
    cls, hdx = _search_jsonable_by_object(obj)
    if cls is not None and hdx is not None:
        data = cls.__jsonable_encode__(obj)
        if isinstance(data, JSONSupportedEditableIters):
            map(directly_encoder, data)

        # { <JSONABLE_PREFIX><class_name>: { 'hash': hash, 'data': data } }
        return {
            f'{JSONABLE_PREFIX}{class_name(obj)}': JSONAbleEncodedDict(hash=hdx, data=data)
        }

    raise ValueError(f'Cannot convert {class_name(class_name(obj), "Unknown")} to JSON')


def directly_decoder(encoded: JSONAbleEncodedDict) -> JSONAbleABC:
    if not has_all_keys(encoded, JSONAbleEncodedDict):
        raise KeyError('Miss key(s)')

    cls = _search_jsonable_by_hash(encoded['hash'])

    if cls is None:
        raise ValueError(
            f'Cannot decode to Python Object'
        )

    return cls.__jsonable_decode__(encoded['data'])


__all__ = (
    'dump', 'dumps', 'load', 'loads', 'register', 'unregister', 'jsonable_encoder', 'JSONAbleDecoder',
    'jsonable_decoder', 'directly_decoder', 'directly_encoder',
    'JSONABLE_PREFIX'
)
