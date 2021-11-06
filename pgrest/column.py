from __future__ import annotations

from typing import Any, Union

from multidict import MultiDict

from pgrest.utils import sanitize_param


class Condition:
    def __init__(self, params: Union[dict, MultiDict]) -> None:
        self.params = MultiDict(params)  # dict of format column: operator.value

    def __and__(self, other: Condition) -> Condition:
        new_params = {
            "and": {**self.params, **other.params}
        }  # TODO: bugs because of possible duplicate and/or keys at the same level of nesting
        return Condition(new_params)

    def __or__(self, other: Condition) -> Condition:
        new_params = {"or": {**self.params, **other.params}}
        return Condition(new_params)

    def flatten_params(self) -> dict[str, str]:
        """parse self.params into a valid query string"""
        check = lambda i: isinstance(i, dict)

        # is the top-level key an "and"/"or"?
        # if it is, there are multiple conditions, nested indefinitely deep
        # travel down, merging them all into a single string
        # if not, there's only a single condition, return directly.
        params = self.params.copy()
        done = {}

        while True:
            top_key, top_value = list(params.items())[0]

    def __repr__(self) -> str:
        return f"<Condition {' '.join([f'{item[0]}={item[1]}' for item in self.params.items()])}>"


class Column:
    """
    Represents a column to use while querying.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __contains__(self, other: Union[list, tuple, set]) -> Condition:
        values = ",".join(map(sanitize_param, other))
        params = {self.name: f"in.({values})"}
        return Condition(params)

    def __eq__(self, other: Any) -> Condition:
        return Condition({self.name: f"eq.{other}"})

    def __ne__(self, other: Any) -> Condition:
        return Condition({self.name: f"neq.{other}"})
