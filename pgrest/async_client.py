from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from httpx import AsyncClient as _AsyncClient

from pgrest.base_client import BaseClient
from pgrest.constants import DEFAULT_POSTGREST_CLIENT_HEADERS
from pgrest.request_builder import FilterRequestBuilder


class Client(BaseClient):
    """Asyncio compatible PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
    ) -> None:
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session: _AsyncClient = _AsyncClient(base_url=base_url, headers=headers)

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
        await self.session.aclose()

    def rpc(self, func: str, params: dict) -> FilterRequestBuilder:
        """Perform a stored procedure call."""
        path = self._get_rpc_path(func)
        return FilterRequestBuilder(self.session, path, "POST", params)
