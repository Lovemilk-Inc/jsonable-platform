from sys import version_info
from typing import TypedDict, TypeAlias, TypeVar, Literal, Union, Generic, Any, Callable, Iterable

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


class JSONAbleABC:
    @classmethod
    def __jsonable_hash__(cls) -> str | None:
        """
        Get the hash of the jsonable object
        :return: Any str or None. if return None, will use the `__name__` of your class
        """
        return

    @classmethod
    def __jsonable_encode__(cls, obj: Self) -> JSONSupportedTypes:
        """
        Encode to json, return native jsonable type
        :parma obj: Any Python object you want to encode
        :return: *The type of return is the same as the `obj` param at function `__jsonable_decode__`
        """
        raise NotImplemented

    @classmethod
    def __jsonable_decode__(cls, data: JSONSupportedTypes) -> Self:
        """
        Decode from json, return any Python object
        :param data: The data of the object, as same as the return of function `__jsonable_encode__`
        :return: Any Python object as same as given at the `obj` param at function `__jsonable_encode__`
        """
        raise NotImplemented


JSONAbleABCType = type[JSONAbleABC]
RequirementsType = Iterable[JSONAbleABCType]


class DefinedClassesData(TypedDict):
    cls: JSONAbleABCType
    requirements: RequirementsType


class DefinedClasses(TypedDict):
    defaults: dict[JSONAbleClassID, DefinedClassesData]
    customs: dict[JSONAbleClassID, DefinedClassesData]


DefinedClassesKeysType = Literal['defaults', 'customs']


class JSONAbleEncodedDict(TypedDict):
    hash: str
    data: JSONSupportedTypes
    source: DefinedClassesKeysType


class RequiredEncodedDict(JSONAbleEncodedDict):
    parent: str


JSONAbleEncodedType = Union[JSONAbleABCEncodedType, RequiredEncodedDict]

HashMethods = Literal['default', 'custom']
EncoderFallbackType = Callable[[Any], JSONAbleEncodedDict]
DecoderFallbackType = Callable[[JSONAbleEncodedDict], Any]
