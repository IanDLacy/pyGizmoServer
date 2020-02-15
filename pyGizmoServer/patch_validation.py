from enum import Enum
from dataclasses import dataclass
from typing import Union, Any, TypeVar, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Op(Enum):
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"


@dataclass
class PatchValidation:
    op: Op
    path: str
    value: Union[bool, float, None, str]

    @staticmethod
    def from_dict(obj: Any) -> "PatchValidation":
        assert isinstance(obj, dict)
        op = Op(obj.get("op"))
        path = from_str(obj.get("path"))
        value = from_union(
            [from_float, from_bool, from_str, from_none], obj.get("value")
        )
        return PatchValidation(op, path, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["op"] = to_enum(Op, self.op)
        result["path"] = from_str(self.path)
        result["value"] = from_union(
            [to_float, from_bool, from_str, from_none], self.value
        )
        return result


def patch_validation_from_dict(s: Any) -> PatchValidation:
    return PatchValidation.from_dict(s)


def patch_validation_to_dict(x: PatchValidation) -> Any:
    return to_class(PatchValidation, x)
