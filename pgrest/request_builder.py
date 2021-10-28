from __future__ import annotations

import re
import sys
from contextlib import suppress
from typing import Any, Awaitable, Iterable, Optional, Union

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from httpx import AsyncClient, Client, Response

from pgrest.utils import sanitize_param, sanitize_pattern_param

CountMethod = Literal["exact", "planned", "estimated"]
RequestMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"]
TableResponse = tuple[Any, Optional[int]]


class RequestBuilder:
    def __init__(self, session: Union[AsyncClient, Client], path: str) -> None:
        """
        Create a RequestBuilder.

        Args:
            session: The httpx session to use to make requests.
            path: The API path to make requests to.
        """
        self.session = session
        self.path = path

    def select(
        self, *columns: str, count: Optional[CountMethod] = None
    ) -> SelectRequestBuilder:
        """
        Run a SELECT query to fetch data.

        Args:
            columns: The names of columns to retrieve. Pass * for all columns.
            count: The method to be used to get the count of records that will be returned.
        Returns:
            [pgrest.request_builder.SelectRequestBuilder][]
        """
        if columns:
            method = "GET"
            self.session.params = self.session.params.set("select", ",".join(columns))
        else:
            method = "HEAD"

        if count:
            self.session.headers["Prefer"] = f"count={count}"

        return SelectRequestBuilder(self.session, self.path, method, {})

    def insert(
        self, row: dict, *, count: Optional[CountMethod] = None, upsert: bool = False
    ) -> QueryRequestBuilder:
        """
        Run an INSERT query to add data to a table.

        Args:
            row: The row to be inserted, as a dictionary, with the column names as keys.
            count:  The method to be used to get the count of records that will be returned.
            upsert: Whether to run an upsert.
        Returns:
            [pgrest.request_builder.QueryRequestBuilder][]
        """
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        if upsert:
            prefer_headers.append("resolution=merge-duplicates")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return QueryRequestBuilder(self.session, self.path, "POST", row)

    def update(
        self, data: dict, *, count: Optional[CountMethod] = None
    ) -> FilterRequestBuilder:
        """
        Run an UPDATE query.

        Args:
            data: The new row data, as a dictionary, with the column names as keys.
            count:  The method to be used to get the count of records that will be returned.
        Returns:
            [pgrest.request_builder.FilterRequestBuilder][]
        """
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return FilterRequestBuilder(self.session, self.path, "PATCH", data)

    def delete(self, *, count: Optional[CountMethod] = None) -> FilterRequestBuilder:
        """
        Run a DELETE query to remove rows from a table.

        Args:
            count:  The method to be used to get the count of records that will be returned.
        Returns:
            [pgrest.request_builder.FilterRequestBuilder][]"""
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return FilterRequestBuilder(self.session, self.path, "DELETE", {})


class QueryRequestBuilder:
    def __init__(
        self,
        session: Union[AsyncClient, Client],
        path: str,
        http_method: RequestMethod,
        json: dict,
    ):
        self.session = session
        self.path = path
        self.http_method: RequestMethod = http_method
        self.json = json

    def _sync_request(
        self, method: RequestMethod, path: str, json: dict
    ) -> Optional[TableResponse]:
        if isinstance(self.session, AsyncClient):
            return

        r = self.session.request(method, path, json=json)
        return self._handle_response(r)

    async def _async_request(
        self, method: RequestMethod, path: str, json: dict
    ) -> Optional[TableResponse]:
        if isinstance(self.session, Client):
            return

        r = await self.session.request(method, path, json=json)
        return self._handle_response(r)

    def _handle_response(self, r: Response) -> tuple[Any, Optional[int]]:
        count = None

        with suppress(KeyError):
            count_header_match = re.search(
                "count=(exact|planned|estimated)", self.session.headers["prefer"]
            )
            content_range = r.headers["content-range"].split("/")
            if count_header_match and len(content_range) >= 2:
                count = int(content_range[1])

        return r.json(), count

    def execute(self) -> Awaitable[Optional[TableResponse]]:
        """Execute a query."""
        if isinstance(self.session, AsyncClient):
            return self._async_request(self.http_method, self.path, json=self.json)
        else:
            return self._sync_request(self.http_method, self.path, json=self.json)  # type: ignore


class FilterRequestBuilder(QueryRequestBuilder):
    def __init__(
        self,
        session: Union[AsyncClient, Client],
        path: str,
        http_method: RequestMethod,
        json: dict,
    ):
        super().__init__(session, path, http_method, json)

        self.negate_next = False

    @property
    def not_(self):
        self.negate_next = True
        return self

    def filter(self, column: str, operator: str, criteria: str):
        """Either filter in or filter out based on Self.negate_next."""
        if self.negate_next is True:
            self.negate_next = False
            operator = f"not.{operator}"
        key, val = sanitize_param(column), f"{operator}.{criteria}"
        self.session.params = self.session.params.add(key, val)
        return self

    def eq(self, column: str, value: str):
        return self.filter(column, "eq", sanitize_param(value))

    def neq(self, column: str, value: str):
        return self.filter(column, "neq", sanitize_param(value))

    def gt(self, column: str, value: str):
        return self.filter(column, "gt", sanitize_param(value))

    def gte(self, column: str, value: str):
        return self.filter(column, "gte", sanitize_param(value))

    def lt(self, column: str, value: str):
        return self.filter(column, "lt", sanitize_param(value))

    def lte(self, column: str, value: str):
        return self.filter(column, "lte", sanitize_param(value))

    def is_(self, column: str, value: str):
        return self.filter(column, "is", sanitize_param(value))

    def like(self, column: str, pattern: str):
        return self.filter(column, "like", sanitize_pattern_param(pattern))

    def ilike(self, column: str, pattern: str):
        return self.filter(column, "ilike", sanitize_pattern_param(pattern))

    def fts(self, column: str, query: str):
        return self.filter(column, "fts", sanitize_param(query))

    def plfts(self, column: str, query: str):
        return self.filter(column, "plfts", sanitize_param(query))

    def phfts(self, column: str, query: str):
        return self.filter(column, "phfts", sanitize_param(query))

    def wfts(self, column: str, query: str):
        return self.filter(column, "wfts", sanitize_param(query))

    def in_(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "in", f"({values})")

    def cs(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "cs", f"{{values}}")

    def cd(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "cd", f"{{values}}")

    def ov(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "ov", f"{{values}}")

    def sl(self, column: str, range: tuple[int, int]):
        return self.filter(column, "sl", f"({range[0]},{range[1]})")

    def sr(self, column: str, range: tuple[int, int]):
        return self.filter(column, "sr", f"({range[0]},{range[1]})")

    def nxl(self, column: str, range: tuple[int, int]):
        return self.filter(column, "nxl", f"({range[0]},{range[1]})")

    def nxr(self, column: str, range: tuple[int, int]):
        return self.filter(column, "nxr", f"({range[0]},{range[1]})")

    def adj(self, column: str, range: tuple[int, int]):
        return self.filter(column, "adj", f"({range[0]},{range[1]})")

    def match(self, query: dict[str, Any]):
        updated_query = None
        for key in query.keys():
            value = query.get(key, "")
            updated_query = self.eq(key, value)
        return updated_query


class SelectRequestBuilder(FilterRequestBuilder):
    def order(self, column: str, *, desc=False, nullsfirst=False):
        self.session.params[
            "order"
        ] = f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}"

        return self

    def limit(self, size: int, *, start=0):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{start + size - 1}"
        return self

    def range(self, start: int, end: int):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{end - 1}"
        return self

    def single(self):
        self.session.headers["Accept"] = "application/vnd.pgrst.object+json"
        return self
