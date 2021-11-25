from datetime import datetime
from json import JSONEncoder as _JSONEncoder
from types import ModuleType
from typing import Any, Callable, Optional
from uuid import UUID


def sanitize_param(param: Any) -> str:
    param = str(param)
    reserved_chars = ",.:()"
    if any(char in param for char in reserved_chars):
        return f"%22{param}%22"
    return param


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(
        pattern.replace("%", "*")
    )  # postgrest specifies to use * instead of %


def check_optional(name: str, obj: Optional[ModuleType]) -> Callable:
    """Decorator to check if a specified optional library is installed."""

    def wrapper(func: Callable) -> Callable:
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            if obj is None:
                raise ImportError(
                    f"You have not installed the {name} dependency. Install it with \npip install pgrest[{name}]"
                )
            else:
                return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


class JSONEncoder(_JSONEncoder):
    # encode datetime, UUID and bytes objects
    def default(self, o: Any) -> str:
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, UUID):
            return str(o)
        elif isinstance(o, bytes):
            return "\\x" + o.hex()
        return super().default(o)
