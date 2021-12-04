from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from httpx import AsyncClient as _AsyncClient

from pgrest.base_client import BaseClient
from pgrest.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class Client(BaseClient):
    """Asyncio compatible PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
        session: Optional[_AsyncClient] = None
    ) -> None:
        """
        Create a PostgREST client.

        Args:
            base_url: base URL of the PostgREST API.
            schema: Which database schema to use.
            headers: Any headers that have to be sent with every request.
            session: instance of httpx.AsyncClient if you want to reuse an existing one.

        !!! tip
            Calling [`Client.fetch_database_types`][pgrest.Client.fetch_database_types] before running any queries, adds some extra
            parsing and validation (for example: timestamp/date/time fields are parsed into proper Python objects automatically)
            by using [Pydantic Models][https://pydantic-docs.helpmanual.io/usage/models] which can be quite convenient.
        """
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session: _AsyncClient = session or _AsyncClient(
            base_url=base_url, headers=headers
        )
        self._models = {}
        self._enums = {}

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """
        Close the underlying HTTP transport and proxies.
        """
        await self.session.aclose()

    async def fetch_database_types(self) -> None:
        """
        Fetch the database models and enumerations from the openapi.json file hosted by PostgREST, and cache them.

        !!! warn
            This method only needs to be called if you want the responses to be parsed into Pydantic objects.
        """
