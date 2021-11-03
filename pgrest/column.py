from __future__ import annotations

from typing import Any, Union

from pgrest.utils import sanitize_param

ParamDict = dict[str, "ParamDict"] | dict[str, str]


class Condition:
    def __init__(self, params: ParamDict) -> None:
        self.params = params  # dict of format column: operator.value

    """ def __and__(self, other: Condition) -> Condition:
        new_value = self._parse_params(other)
        self.params = {"and": new_value}
        return self

    def __or__(self, other: Condition) -> Condition:
        new_value = self._parse_params(other)
        self.params = {"or": new_value}
        return self

    def _parse_params(self, other: Condition) -> str:
        # parse the params to form new params
        new_value = ""
        if len(other.params) == 1:  # only one key, possibly AND/OR
            top_key, top_value = list(other.params.items())[0]
            if top_key in ["and", "or"]:
                # no longer a top-level param
                # their value has to be wrapped into parentheses
                new_value += f",{top_key}"
                new_value += f"({top_value})"
            else: # normal condition
                new_value += f",{top_key}.{top_value}"
        else:
            new_value += "," + ",".join([".".join(item) for item in other.params.items()])

        if len(self.params) == 1:
            top_key, top_value = list(self.params.items())[0]
            if top_key in ["and", "or"]:
                # no longer a top-level param
                # their value has to be wrapped into parentheses
                new_value += f",{top_key}"
                new_value += f"({top_value})"
            else: # normal condition
                new_value += f",{top_key}.{top_value}"
        else:
            new_value += "," + ",".join([".".join(item) for item in self.params.items()])

        return new_value"""

    def __and__(self, other: Condition) -> Condition:
        new_params = {"and": {**self.params, **other.params}}
        return Condition(new_params)

    def __or__(self, other: Condition) -> Condition:
        new_params = {"or": {**self.params, **other.params}}
        return Condition(new_params)

    def flatten_params(self) -> dict[str, str]:
        """parse self.params into a valid query string"""
        raise NotImplementedError

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
