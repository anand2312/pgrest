from datetime import date, datetime, time
from enum import Enum
from typing import Dict, List, Tuple
from uuid import UUID

from httpx import Response
from pydantic import BaseModel

TYPE_MAP = {
    "bigint": int,
    "smallint": int,
    "integer": int,
    "timestamp with time zone": datetime,
    "timestamp without time zone": datetime,
    "date": date,
    "time with time zone": time,
    "time without time zone": time,
    "real": float,
    "json": dict,  # TODO: confirm this!
    "jsonb": dict,
    "text": str,
    "character varying": str,
    "uuid": UUID,
    "boolean": bool,
    "ARRAY": list,
}


def parse_openapi_data(
    schema: str, res: Response
) -> Tuple[Dict[str, BaseModel], Dict[str, Enum]]:
    ...


def get_model_name(table: str) -> str:
    """
    Generally, Postgres tables are named in snake_case, but models being classes should be named in PascalCase.
    This function returns the equivalent PascalCase name of a snake_case table.
    """
    words = table.split("_")
    if len(words) == 1:
        return table.title()
    else:
        return "".join(map(str.title, words))


def get_enum_name(old_name: str, schema: str = "public") -> str:
    """
    Enums are named as <schema>.<enumname> in the openapi.json returned by postgrest.
    """
    return old_name.replace(
        schema, ""
    ).title()  # new in py3.9 - str.removesuffix/removeprefix


def create_enum(name: str, fields: List[str], schema: str = "public") -> Enum:
    name = get_enum_name(name, schema)
    enum_keys = map(
        str.upper, map(str.strip, fields)
    )  # remove whitespace and turn to uppercase
    enum_fields = zip(enum_keys, fields)
    return Enum(name, enum_fields)
