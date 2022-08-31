from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from typing_extensions import Protocol

from . import operators
from .base import SchemaEventTarget
from .elements import ClauseElement
from .sqltypes import Boolean
from .sqltypes import Indexable
from .sqltypes import Integer
from .sqltypes import MatchType
from .sqltypes import NullType
from .sqltypes import String
from .sqltypes import TableValueType
from .visitors import Traversible
from .visitors import TraversibleType
from .. import util
from ..engine import Dialect
from ..util import compat

BOOLEANTYPE: Boolean
INTEGERTYPE: Integer
NULLTYPE: NullType
STRINGTYPE: String
MATCHTYPE: MatchType
INDEXABLE = Indexable
TABLEVALUE: TableValueType

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_U = TypeVar("_U")

_TE = TypeVar("_TE", bound=TypeEngine[Any])
_NFE = TypeVar("_NFE", bound=NativeForEmulated)
_UDT = TypeVar("_UDT", bound=UserDefinedType[Any])
_TD = TypeVar("_TD", bound=TypeDecorator[Any])
_VT = TypeVar("_VT", bound=Variant[Any])

class _LiteralProcessor(Protocol[_T_contra]):
    def __call__(self, __value: Optional[_T_contra]) -> str: ...

class _BindProcessor(Protocol[_T_contra]):
    def __call__(self, __value: Optional[_T_contra]) -> Optional[Any]: ...

class _ResultProcessor(Protocol[_T_co]):
    def __call__(self, __value: Optional[Any]) -> Optional[_T_co]: ...

class TypeEngine(Traversible, Generic[_T]):
    __visit_name__: ClassVar[str] = ...
    class Comparator(operators.ColumnOperators, Generic[_TE]):
        default_comparator: Any = ...
        def __clause_element__(self) -> ClauseElement: ...
        expr: ClauseElement = ...
        type: _TE = ...
        def __init__(self, expr: ClauseElement) -> None: ...
        def operate(
            self, op: Any, *other: Any, **kwargs: Any
        ) -> ClauseElement: ...
        def reverse_operate(
            self, op: Any, other: Any, **kwargs: Any
        ) -> ClauseElement: ...
        def __reduce__(self) -> Any: ...
    hashable: bool = ...
    comparator_factory: Type[Comparator[TypeEngine[_T]]] = ...
    sort_key_function: Optional[compat._SortKeyFunction] = ...
    should_evaluate_none: bool = ...
    def evaluates_none(self: _TE) -> _TE: ...
    def copy(self: _TE, **kw: Any) -> _TE: ...
    def compare_against_backend(
        self, dialect: Dialect, conn_type: Any
    ) -> Any: ...
    def copy_value(self, value: _T) -> _T: ...
    def literal_processor(
        self, dialect: Dialect
    ) -> Optional[_LiteralProcessor[_T]]: ...
    def bind_processor(
        self, dialect: Dialect
    ) -> Optional[_BindProcessor[_T]]: ...
    def result_processor(
        self, dialect: Dialect, coltype: Any
    ) -> Optional[_ResultProcessor[_T]]: ...
    def column_expression(self, colexpr: Any) -> Any: ...
    def bind_expression(self, bindvalue: Any) -> Any: ...
    def compare_values(self, x: Any, y: Any) -> bool: ...
    def get_dbapi_type(self, dbapi: Any) -> Any: ...
    @property
    def python_type(self) -> Type[_T]: ...
    def with_variant(
        self, type_: Type[TypeEngine[_U]], dialect_name: str
    ) -> Variant[_U]: ...
    def as_generic(self, allow_nulltype: bool = ...) -> TypeEngine[Any]: ...
    def dialect_impl(self, dialect: Dialect) -> Type[Any]: ...
    def adapt(self, __cls: Type[_U], **kw: Any) -> _U: ...
    def coerce_compared_value(
        self, op: Any, value: Any
    ) -> TypeEngine[Any]: ...
    def compile(self, dialect: Optional[Dialect] = ...) -> Any: ...

class VisitableCheckKWArg(util.EnsureKWArgType, TraversibleType): ...

class UserDefinedType(TypeEngine[_T], metaclass=VisitableCheckKWArg):
    ensure_kwarg: str = ...
    def coerce_compared_value(self: _UDT, op: Any, value: Any) -> _UDT: ...

class Emulated:
    def adapt_to_emulated(self, impltype: Any, **kw: Any) -> Any: ...
    def adapt(self, __impltype: Any, **kw: Any) -> Any: ...

class NativeForEmulated:
    @classmethod
    def adapt_native_to_emulated(cls, impl: Any, **kw: Any) -> Any: ...
    @classmethod
    def adapt_emulated_to_native(
        cls: Type[_NFE], impl: Any, **kw: Any
    ) -> _NFE: ...

class TypeDecorator(SchemaEventTarget, TypeEngine[_T]):
    impl: Any = ...
    cache_ok: ClassVar[Optional[bool]] = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    coerce_to_is_types: Tuple[Type[Any], ...] = ...
    class Comparator(TypeEngine.Comparator[_TE]):
        def operate(
            self, op: Any, *other: Any, **kwargs: Any
        ) -> ClauseElement: ...
        def reverse_operate(
            self, op: Any, other: Any, **kwargs: Any
        ) -> ClauseElement: ...
    @property
    def comparator_factory(self) -> Type[Comparator[TypeEngine[_T]]]: ...  # type: ignore[override]
    def type_engine(self, dialect: Dialect) -> TypeEngine[Any]: ...
    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]: ...
    def __getattr__(self, key: Any) -> Any: ...
    def process_literal_param(
        self, value: Optional[_T], dialect: Dialect
    ) -> str: ...
    def process_bind_param(
        self, value: Optional[_T], dialect: Dialect
    ) -> Any: ...
    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Optional[_T]: ...
    def literal_processor(self, dialect: Dialect) -> _LiteralProcessor[_T]: ...
    def bind_processor(self, dialect: Dialect) -> _BindProcessor[_T]: ...
    def result_processor(
        self, dialect: Dialect, coltype: Any
    ) -> _ResultProcessor[_T]: ...
    def bind_expression(self, bindparam: Any) -> Any: ...
    def column_expression(self, column: Any) -> Any: ...
    def coerce_compared_value(self, op: Any, value: Any) -> Any: ...
    def copy(self: _TD, **kw: Any) -> _TD: ...
    def get_dbapi_type(self, dbapi: Any) -> Any: ...
    def compare_values(self, x: Any, y: Any) -> bool: ...
    @property
    def sort_key_function(self) -> Optional[compat._SortKeyFunction]: ...  # type: ignore[override]

class Variant(TypeDecorator[_T]):
    impl: TypeEngine[Any] = ...
    mapping: Mapping[str, TypeEngine[Any]] = ...
    def __init__(
        self, base: Any, mapping: Mapping[str, TypeEngine[Any]]
    ) -> None: ...
    def coerce_compared_value(
        self: _VT, operator: Any, value: Any
    ) -> Union[_VT, TypeEngine[Any]]: ...
    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]: ...
    def with_variant(
        self, type_: Type[TypeEngine[_U]], dialect_name: str
    ) -> Variant[_U]: ...
    @property
    def comparator_factory(self) -> Type[Any]: ...  # type: ignore[override]

def to_instance(typeobj: Any, *arg: Any, **kw: Any) -> Any: ...
def adapt_type(typeobj: Any, colspecs: Any) -> Any: ...

TypingBindProcessor = _BindProcessor
TypingLiteralProcessor = _LiteralProcessor
TypingResultProcessor = _ResultProcessor
