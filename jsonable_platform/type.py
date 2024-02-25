from sys import version_info
from typing import TypedDict, TypeAlias, TypeVar, Literal, Union, Generic, Any, Callable

JSONAbleClassID: TypeAlias = str

JSONSupportedBases: TypeAlias = Union[bytes, str, int, float, bool, None]
JSONSupportedIterables: TypeAlias = Union[
    list[Union[JSONSupportedBases, 'JSONSupportedIterables', 'JSONAbleABC']],
    tuple[Union[JSONSupportedBases, 'JSONSupportedIterables', 'JSONAbleABC']],
    dict[
        Union[JSONSupportedBases, 'JSONSupportedIterables'],
        Union[JSONSupportedBases, 'JSONSupportedIterables', 'JSONAbleABC']
    ]
]
JSONSupportedEditableIters: TypeAlias = Union[list, dict]

JSONSupportedTypes: TypeAlias = Union[JSONSupportedBases, JSONSupportedIterables]

# `Self` is Python 3.11+ Only (https://docs.python.org/zh-cn/3/library/typing.html#typing.Self)
if version_info >= (3, 11):
    from typing import Self  # type: ignore
else:
    from typing_extensions import Self

JSONAbleABCEncodedType = TypeVar('JSONAbleABCEncodedType', bound=JSONSupportedTypes)


class JSONAbleABC(Generic[JSONAbleABCEncodedType]):
    @classmethod
    def __jsonable_hash__(cls) -> str | None:
        """
        Get the hash of the jsonable object
        :return: Any str or None. if return None, will use the `__name__` of your class
        """
        return

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONAbleABCEncodedType:
        """
        Encode to json, return native jsonable type
        :parma obj: Any Python object you want to encode
        :return: *The type of return is the same as the `obj` param at function `__jsonable_decode__`
        """
        raise NotImplemented

    @classmethod
    def __jsonable_decode__(cls, data: JSONAbleABCEncodedType) -> Self:
        """
        Decode from json, return any Python object
        :param data: The data of the object, as same as the return of function `__jsonable_encode__`
        :return: Any Python object as same as given at the `obj` param at function `__jsonable_encode__`
        """
        raise NotImplemented


class DefinedClasses(TypedDict):
    names: dict[JSONAbleClassID, type[JSONAbleABC]]
    classes: dict[JSONAbleClassID, type[JSONAbleABC]]


class JSONAbleEncodedDict(TypedDict):
    hash: str
    data: JSONSupportedTypes


HashMethods = Literal['default', 'custom']
EncoderFallbackType = Callable[[Any], JSONAbleEncodedDict]
DecoderFallbackType = Callable[[JSONAbleEncodedDict], Any]
