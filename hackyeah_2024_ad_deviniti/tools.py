from typing import Optional, TypeVar

_V = TypeVar("_V")


def require_value(value: Optional[_V]) -> _V:
    if value is not None:
        return value
    else:
        raise Exception("Value is None")
