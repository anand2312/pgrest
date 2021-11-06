from __future__ import annotations

from numbers import Number
from typing import Any, Iterable, Optional, Union, cast

from multidict import MultiDict

from pgrest.utils import sanitize_param, sanitize_pattern_param

RecursiveDict = Union[dict[str, str], dict[str, "RecursiveDict"]]  # base case


class Column:
    """
    Represents a column to use while querying.

    !!! tip
        Refer the [PostgREST docs](https://postgrest.org/en/v8.0/api.html?highlight=filters#operators) for more info about operators.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: Any) -> Condition:
        return Condition({self.name: f"eq.{sanitize_param(other)}"})

    def __ne__(self, other: Any) -> Condition:
        return Condition({self.name: f"neq.{sanitize_param(other)}"})

    def __gt__(self, other: Number) -> Condition:
        return Condition({self.name: f"gt.{sanitize_param(other)}"})

    def __ge__(self, other: Number) -> Condition:
        return Condition({self.name: f"gte.{sanitize_param(other)}"})

    def __lt__(self, other: Number) -> Condition:
        return Condition({self.name: f"lt.{sanitize_param(other)}"})

    def __le__(self, other: Number) -> Condition:
        return Condition({self.name: f"lte.{sanitize_param(other)}"})

    def __lshift__(self, _range: Union[tuple[int, int], range]) -> Condition:
        if isinstance(_range, range):
            low, hi = _range.start, _range.stop
        elif isinstance(_range, tuple):
            low, hi = _range
        else:
            raise TypeError(
                f"Invalid input for operator `sl`; expected range or two-tuple of ints, got {type(_range)}"
            )
        return Condition({self.name: f"sl.({low},{hi})"})

    def __rshift__(self, _range: Union[tuple[int, int], range]) -> Condition:
        if isinstance(_range, range):
            low, hi = _range.start, _range.stop
        elif isinstance(_range, tuple):
            low, hi = _range
        else:
            raise TypeError(
                f"Invalid input for operator `sr`; expected range or two-tuple of ints, got {type(_range)}"
            )
        return Condition({self.name: f"sr.({low},{hi})"})

    def __matmul__(self, other: str) -> Condition:
        return Condition({self.name: f"fts.{sanitize_param(other)}"})

    def eq(self, value: str) -> Condition:
        """
        Operator: "equals to"

        !!! note
            This is an alternative to doing `Column(x) == value`
        """
        return Condition({self.name: f"eq.{sanitize_param(value)}"})

    def neq(self, value: str) -> Condition:
        """
        Operator: "not equal to"

        !!! note
            This is an alternative to doing `Column(x) != value`
        """
        return Condition({self.name: f"neq.{sanitize_param(value)}"})

    def gt(self, value: str) -> Condition:
        """
        Operator: "greater than"

        !!! note
            This is an alternative to doing `Column(x) > value`
        """
        return Condition({self.name: f"gt.{sanitize_param(value)}"})

    def gte(self, value: str) -> Condition:
        """
        Operator: "greater than or equal to"

        !!! note
            This is an alternative to doing `Column(x) >= value`
        """
        return Condition({self.name: f"gte.{sanitize_param(value)}"})

    def lt(self, value: str) -> Condition:
        """
        Operator: "less than"

        !!! note
            This is an alternative to doing `Column(x) < value`
        """
        return Condition({self.name: f"ltq.{sanitize_param(value)}"})

    def lte(self, value: str) -> Condition:
        """
        Operator: "less than or equal to"

        !!! note
            This is an alternative to doing `Column(x) <= value`
        """
        return Condition({self.name: f"lte.{sanitize_param(value)}"})

    def is_(self, value: Optional[bool]) -> Condition:
        """
        Compares for exact equality (for null/true/false).
        """
        if isinstance(value, bool):
            val = str(value).lower()
        else:
            val = "null"
        return Condition({self.name: f"is.{sanitize_param(val)}"})

    def like(self, pattern: str) -> Condition:
        """
        SQL "LIKE" operator.
        """
        return Condition({self.name: f"like.{sanitize_pattern_param(pattern)}"})

    def ilike(self, pattern: str) -> Condition:
        """
        Case insensitive "LIKE" operator.
        """
        return Condition({self.name: f"ilike.{sanitize_pattern_param(pattern)}"})

    def in_(self, values: Iterable) -> Condition:
        """
        Check if the column value is one of a list of values.
        """
        values = map(sanitize_param, values)
        return Condition({self.name: f"in.({','.join(values)})"})

    def fts(self, query: str) -> Condition:
        """
        Full-text search using [to_tsquery](https://www.postgresql.org/docs/12/functions-textsearch.html)
        """
        return Condition({self.name: f"fts.{sanitize_param(query)}"})

    def plfts(self, query: str) -> Condition:
        """
        Operator: Full-Text search using [plainto_tsquery](https://www.postgresql.org/docs/12/functions-textsearch.html)
        """
        return Condition({self.name: f"plfts.{sanitize_param(query)}"})

    def phfts(self, query: str) -> Condition:
        """
        Operator: Full-Text search using [phraseto_tsquery](https://www.postgresql.org/docs/12/functions-textsearch.html)
        """
        return Condition({self.name: f"phfts.{sanitize_param(query)}"})

    def wfts(self, query: str) -> Condition:
        """
        Operator: Full-Text search using [websearch_to_tsquery](https://www.postgresql.org/docs/12/functions-textsearch.html)
        """
        return Condition({self.name: f"wfts.{sanitize_param(query)}"})

    def cs(self, values: Iterable[str]) -> Condition:
        """
        Operator: contains
        """
        values = map(sanitize_param, values)
        values = ",".join(values)
        return Condition({self.name: f"cs.{{values}}"})

    def cd(self, values: Iterable[str]) -> Condition:
        """
        Operator: contained in
        """
        values = map(sanitize_param, values)
        values = ",".join(values)
        return Condition({self.name: f"cd.{{values}}"})

    def ov(self, values: Iterable[str]) -> Condition:
        """
        Operator: overlap (have points in common)
        """
        values = map(sanitize_param, values)
        values = ",".join(values)
        return Condition({self.name: f"ov.{{values}}"})

    def sl(self, range: tuple[int, int]) -> Condition:
        """
        Operator: strictly left of

        !!! note
            This is an alternative to doing `Column(x) << (f1, f2)`
        """
        return Condition({self.name: f"sl.({range[0]},{range[1]})"})

    def sr(self, range: tuple[int, int]) -> Condition:
        """
        Operator: strictly right of

        !!! note
            This is an alternative to doing `Column(x) >> (f1, f2)`
        """
        return Condition({self.name: f"sr.({range[0]},{range[1]})"})

    def nxl(self, range: tuple[int, int]) -> Condition:
        """
        Operator: does not extend to the left of
        """
        return Condition({self.name: f"nxl.({range[0]},{range[1]})"})

    def nxr(self, range: tuple[int, int]) -> Condition:
        """
        Operator: does not extend to the right of
        """
        return Condition({self.name: f"nxr.({range[0]},{range[1]})"})

    def adj(self, range: tuple[int, int]) -> Condition:
        """
        Operator: is adjacent to
        """
        return Condition({self.name: f"nxr.({range[0]},{range[1]})"})


class Condition:
    """
    Represents a query condition.

    !!! warning
        This class is not meant to be constructed directly, nor is it part of the public API of this library.
        Instances of this class are returned by methods on the [Column][pgrest.query.Column] class, and is documented here
        for the sake of clarity only.
    """

    def __init__(self, params: Union[dict, MultiDict]) -> None:
        self.params = MultiDict(params)  # dict of format column: operator.value

    def __and__(self, other: Condition) -> Condition:
        """Join multiple conditions using AND"""
        self_params, other_params = MultiDict(self.params), MultiDict(other.params)
        self_params.extend(other_params)
        new_params = {"and": self_params}
        return Condition(new_params)

    def __or__(self, other: Condition) -> Condition:
        """Join multiple conditions using OR"""
        self_params, other_params = MultiDict(self.params), MultiDict(other.params)
        self_params.extend(other_params)
        new_params = {"or": self_params}
        return Condition(new_params)

    def flatten_params(self) -> dict[str, str]:
        """parse self.params into a valid query string"""
        top_key, top_val = list(self.params.items())[0]

        if top_key in {"and", "or"}:
            return {top_key: Condition.stringify(top_val)}
        else:
            return {top_key: top_val}

    @staticmethod
    def stringify(obj: RecursiveDict) -> str:
        """recursively convert each dictionary into a string"""
        done = []
        for key, val in obj.items():
            if key in {"and", "or"}:
                dict_as_str = Condition.stringify(cast(RecursiveDict, val))
                done.append(f"{key}({dict_as_str})")
                continue
            done.append(f"{key}.{val}")
        else:
            return ",".join(done)

    def __repr__(self) -> str:
        return f"<Condition {' '.join([f'{item[0]}={item[1]}' for item in self.params.items()])}>"
